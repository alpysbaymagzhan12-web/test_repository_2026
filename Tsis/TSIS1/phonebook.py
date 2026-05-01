# phonebook.py — TSIS 1
import csv
import json
import os
import psycopg2
from connect import get_connection, init_schema

# Подключаемся к базе данных
conn = get_connection()
cur = conn.cursor()

# Создаём таблицы если их нет
init_schema()


# ─────────────────────────────────────────
# Вспомогательная функция — печатает список контактов
# ─────────────────────────────────────────
def show_contacts(rows):
    if not rows:
        print("Контакты не найдены")
        return
    print("-" * 60)
    for r in rows:
        print(f"Имя     : {r[0]}")
        print(f"Email   : {r[1] or '—'}")
        print(f"День рож: {r[2] or '—'}")
        print(f"Группа  : {r[3] or '—'}")
        print(f"Телефоны: {r[4] or '—'}")
        print("-" * 60)


# ─────────────────────────────────────────
# 1. Фильтр по группе
# ─────────────────────────────────────────
def filter_by_group():
    group = input("Введи название группы: ").strip()

    cur.execute("""
        SELECT c.username, c.email, c.birthday, g.name,
               STRING_AGG(ph.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g  ON g.id = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        WHERE g.name ILIKE %s
        GROUP BY c.username, c.email, c.birthday, g.name
        ORDER BY c.username
    """, (f"%{group}%",))

    show_contacts(cur.fetchall())


# ─────────────────────────────────────────
# 2. Поиск по email
# ─────────────────────────────────────────
def search_by_email():
    email = input("Введи часть email: ").strip()

    cur.execute("""
        SELECT c.username, c.email, c.birthday, g.name,
               STRING_AGG(ph.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g  ON g.id = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        WHERE c.email ILIKE %s
        GROUP BY c.username, c.email, c.birthday, g.name
        ORDER BY c.username
    """, (f"%{email}%",))

    show_contacts(cur.fetchall())


# ─────────────────────────────────────────
# 3. Показать всех с сортировкой
# ─────────────────────────────────────────
def show_all_sorted():
    print("Сортировка:")
    print("  1 - По имени")
    print("  2 - По дню рождения")
    print("  3 - По дате добавления")
    choice = input(">> ").strip()

    if choice == "2":
        order = "c.birthday"
    elif choice == "3":
        order = "c.created_at"
    else:
        order = "c.username"

    cur.execute(f"""
        SELECT c.username, c.email, c.birthday, g.name,
               STRING_AGG(ph.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g  ON g.id = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        GROUP BY c.username, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order}
    """)

    show_contacts(cur.fetchall())


# ─────────────────────────────────────────
# 4. Листать страницами (next / prev / quit)
# ─────────────────────────────────────────
def browse_pages():
    page_size = 3  # сколько контактов на одной странице
    page = 0       # текущая страница (начинаем с 0)

    while True:
        offset = page * page_size  # сколько пропустить

        cur.execute("""
            SELECT c.username, c.email, c.birthday, g.name,
                   STRING_AGG(ph.phone, ', ')
            FROM contacts c
            LEFT JOIN groups g  ON g.id = c.group_id
            LEFT JOIN phones ph ON ph.contact_id = c.id
            GROUP BY c.username, c.email, c.birthday, g.name
            ORDER BY c.username
            LIMIT %s OFFSET %s
        """, (page_size, offset))

        rows = cur.fetchall()

        print(f"\n=== Страница {page + 1} ===")
        show_contacts(rows)

        nav = input("[n] следующая  [p] предыдущая  [q] выход >> ").strip().lower()

        if nav == "q":
            break
        elif nav == "n":
            if len(rows) < page_size:
                print("Это последняя страница")
            else:
                page += 1
        elif nav == "p":
            if page == 0:
                print("Это первая страница")
            else:
                page -= 1


# ─────────────────────────────────────────
# 5. Экспорт в JSON
# ─────────────────────────────────────────
def export_to_json():
    # Получаем все контакты из базы
    cur.execute("""
        SELECT c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.username
    """)
    contacts = cur.fetchall()

    result = []
    for username, email, birthday, group in contacts:
        # Для каждого контакта получаем его телефоны
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = (SELECT id FROM contacts WHERE username = %s)", (username,))
        phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]

        result.append({
            "username": username,
            "email":    email,
            "birthday": str(birthday) if birthday else None,
            "group":    group,
            "phones":   phones
        })

    filename = input("Имя файла [export.json]: ").strip() or "export.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Экспортировано {len(result)} контактов в {filename}")


# ─────────────────────────────────────────
# 6. Импорт из JSON
# ─────────────────────────────────────────
def import_from_json():
    filename = input("Имя файла [export.json]: ").strip() or "export.json"

    if not os.path.exists(filename):
        print("Файл не найден")
        return

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    inserted = 0
    skipped = 0

    for contact in data:
        username = contact.get("username", "").strip()
        if not username:
            continue

        # Проверяем — есть ли уже такой контакт
        cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
        exists = cur.fetchone()

        if exists:
            answer = input(f"'{username}' уже есть. [s] пропустить / [o] перезаписать: ").strip().lower()
            if answer != "o":
                skipped += 1
                continue
            # Удаляем старый (телефоны удалятся автоматически — CASCADE)
            cur.execute("DELETE FROM contacts WHERE username = %s", (username,))

        # Находим или создаём группу
        group_id = None
        if contact.get("group"):
            cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING", (contact["group"],))
            cur.execute("SELECT id FROM groups WHERE name = %s", (contact["group"],))
            group_id = cur.fetchone()[0]

        # Вставляем контакт
        cur.execute(
            "INSERT INTO contacts(username, email, birthday, group_id) VALUES(%s, %s, %s, %s) RETURNING id",
            (username, contact.get("email"), contact.get("birthday"), group_id)
        )
        contact_id = cur.fetchone()[0]

        # Вставляем телефоны
        for ph in contact.get("phones", []):
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES(%s, %s, %s)",
                (contact_id, ph["phone"], ph.get("type", "mobile"))
            )

        inserted += 1

    conn.commit()  # сохраняем все изменения
    print(f"Готово: вставлено {inserted}, пропущено {skipped}")


# ─────────────────────────────────────────
# 7. Импорт из CSV
# ─────────────────────────────────────────
def import_from_csv():
    filename = input("Имя файла [contacts.csv]: ").strip() or "contacts.csv"

    if not os.path.exists(filename):
        print("Файл не найден")
        return

    inserted = 0
    errors = 0

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row.get("username", "").strip()
            if not username:
                errors += 1
                continue

            # Пропускаем если уже есть
            cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
            if cur.fetchone():
                continue

            # Находим или создаём группу
            group_id = None
            if row.get("group"):
                cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING", (row["group"],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (row["group"],))
                group_id = cur.fetchone()[0]

            # Вставляем контакт
            cur.execute(
                "INSERT INTO contacts(username, email, birthday, group_id) VALUES(%s, %s, %s, %s) RETURNING id",
                (username, row.get("email") or None, row.get("birthday") or None, group_id)
            )
            contact_id = cur.fetchone()[0]

            # Вставляем телефон
            if row.get("phone"):
                phone_type = row.get("phone_type", "mobile")
                if phone_type not in ("home", "work", "mobile"):
                    phone_type = "mobile"
                cur.execute(
                    "INSERT INTO phones(contact_id, phone, type) VALUES(%s, %s, %s)",
                    (contact_id, row["phone"], phone_type)
                )

            inserted += 1

    conn.commit()  # сохраняем все изменения
    print(f"Импортировано {inserted} контактов, ошибок {errors}")


# ─────────────────────────────────────────
# 8. Добавить новый контакт
# ─────────────────────────────────────────
def add_contact():
    username = input("Username (имя): ").strip()
    if not username:
        print("Username не может быть пустым")
        return

    # Проверяем — вдруг уже есть такой
    cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
    if cur.fetchone():
        print(f"Контакт '{username}' уже существует")
        return

    email    = input("Email (Enter чтобы пропустить): ").strip() or None
    birthday = input("День рождения (2000-01-01) (Enter чтобы пропустить): ").strip() or None
    group    = input("Группа (Family/Work/Friend/Other): ").strip() or None
    phone    = input("Телефон: ").strip() or None
    ph_type  = input("Тип телефона (home/work/mobile): ").strip() or "mobile"

    try:
        # Находим или создаём группу
        group_id = None
        if group:
            cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING", (group,))
            cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
            group_id = cur.fetchone()[0]

        # Вставляем контакт
        cur.execute(
            "INSERT INTO contacts(username, email, birthday, group_id) VALUES(%s, %s, %s, %s) RETURNING id",
            (username, email, birthday, group_id)
        )
        contact_id = cur.fetchone()[0]

        # Вставляем телефон если указан
        if phone:
            if ph_type not in ("home", "work", "mobile"):
                ph_type = "mobile"
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES(%s, %s, %s)",
                (contact_id, phone, ph_type)
            )

        conn.commit()  # сохраняем
        print(f"Контакт '{username}' добавлен!")

    except psycopg2.Error as e:
        conn.rollback()  # отменяем если ошибка
        print(f"Ошибка: {e}")


# ─────────────────────────────────────────
# 9. Добавить телефон (вызов процедуры из БД)
# ─────────────────────────────────────────
def add_phone():
    username = input("Username контакта: ").strip()
    phone    = input("Номер телефона   : ").strip()
    ph_type  = input("Тип (home/work/mobile): ").strip() or "mobile"

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (username, phone, ph_type))
        conn.commit()  # сохраняем
        print("Телефон добавлен!")
    except psycopg2.Error as e:
        conn.rollback()  # отменяем если ошибка
        print(f"Ошибка: {e}")


# ─────────────────────────────────────────
# 10. Переместить в группу (вызов процедуры из БД)
# ─────────────────────────────────────────
def move_to_group():
    username = input("Username контакта: ").strip()
    group    = input("Название группы  : ").strip()

    try:
        cur.execute("CALL move_to_group(%s, %s)", (username, group))
        conn.commit()  # сохраняем
        print("Контакт перемещён!")
    except psycopg2.Error as e:
        conn.rollback()  # отменяем если ошибка
        print(f"Ошибка: {e}")


# ─────────────────────────────────────────
# 11. Поиск по имени / email / телефону (функция из БД)
# ─────────────────────────────────────────
def search_contacts():
    query = input("Поисковый запрос: ").strip()

    try:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        show_contacts(cur.fetchall())
    except psycopg2.Error as e:
        print(f"Ошибка: {e}")


# ─────────────────────────────────────────
# Главное меню
# ─────────────────────────────────────────
while True:
    print("""
=== PhoneBook — TSIS 1 ===
 1. Фильтр по группе
 2. Поиск по email
 3. Показать всех (с сортировкой)
 4. Листать страницами
 5. Экспорт в JSON
 6. Импорт из JSON
 7. Импорт из CSV
 8. Добавить новый контакт
 9. Добавить телефон к контакту
10. Переместить в группу
11. Поиск (имя / email / телефон)
 q. Выход
""")

    choice = input(">> ").strip()

    if   choice == "1":  filter_by_group()
    elif choice == "2":  search_by_email()
    elif choice == "3":  show_all_sorted()
    elif choice == "4":  browse_pages()
    elif choice == "5":  export_to_json()
    elif choice == "6":  import_from_json()
    elif choice == "7":  import_from_csv()
    elif choice == "8":  add_contact()
    elif choice == "9":  add_phone()
    elif choice == "10": move_to_group()
    elif choice == "11": search_contacts()
    elif choice == "q":  break
    else:                print("Неизвестная команда")

cur.close()
conn.close()