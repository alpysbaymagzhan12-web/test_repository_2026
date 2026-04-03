import psycopg2
import csv
from config import parametrs

def get_conn():
    return psycopg2.connect(
        host=parametrs['host'].strip(),
        database=parametrs['database'].strip(),
        user=parametrs['user'].strip(),
        password=parametrs['password'].strip()
    )

def crate_table():
    with get_conn() as conn:
        with conn.cursor() as f:
            f.execute('''
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(250),
                    phone VARCHAR(25)
                );
            ''')
        conn.commit()

def insetr_csv(file):
    with get_conn() as conn:
        with conn.cursor() as c:
            with open(file, 'r', encoding='utf-8') as f:
                r = csv.reader(f)
                for row in r:
                    c.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", row)
        conn.commit()

def add_contact(name, phone):
    with get_conn() as conn:
        with conn.cursor() as throw:
            throw.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()

def update_contact(name, new_phone):
    with get_conn() as conn:
        with conn.cursor() as update:
            update.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))
        conn.commit()

def contact_find(soz):
    with get_conn() as conn:
        with conn.cursor() as throw:
            throw.execute("SELECT * FROM phonebook WHERE name LIKE %s OR phone LIKE %s", (f'%{soz}%', f'{soz}%'))
            res = throw.fetchall()
            if res:
                for row in res: print(row)

def contact_del(name):
    with get_conn() as conn:
        with conn.cursor() as throw:
            throw.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        conn.commit()
def see_all():
    with get_conn() as conn:
        with conn.cursor()as throw:
            throw.execute("select*from phonebook")
            rows=throw.fetchall()
            for row in rows:
                print(row)
    conn.commit()

def menu():
    crate_table()
    while True:
        print("\n1: CSV | 2: Add | 3: Update | 4: Find | 5: Delete |6: See al persons | 0: Exit")
        sol = input("Choice: ")
        if sol == '1': insetr_csv('contacts.csv')
        elif sol == '2': add_contact(input("Name: "), input("Phone: "))
        elif sol == '3': update_contact(input("Name: "), input("New Phone: "))
        elif sol == '4': contact_find(input("Search: "))
        elif sol == '5': contact_del(input("Name: "))
        elif sol == '6': see_all()
        elif sol == '0': break

if __name__ == "__main__":
    menu()