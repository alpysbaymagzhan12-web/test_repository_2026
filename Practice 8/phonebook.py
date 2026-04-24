import psycopg2
from config import parametrs
def execute_Sql_file(file_sql,connecttion):
    with open(file_sql,"r") as file:
        sql_commands = file.read()
    with connecttion.cursor() as cur:
        cur.execute(sql_commands)
        connecttion.commit()
def get_con():
    return psycopg2.connect(
        host=parametrs['host'],
        database=parametrs['database'],
        user=parametrs['user'],
        password=parametrs['password']
    )
def create_table():#---------------------------------------------------------------------
    with get_con() as conn:
        with conn.cursor() as throw:
            throw.execute('''CREATE TABLE IF NOT EXISTS  phonebook_pr8(
                          id SERIAL PRIMARY KEY,
                          name VARCHAR(200) UNIQUE,
                          phone VARCHAR(20)
                          );'''
                          )
        conn.commit()         
def see_phonebook_pr8():#---------------------------------------------------------------------
    with get_con() as conn:
        with conn.cursor() as throw:
            throw.execute("select*from phonebook_pr8")
            rows=throw.fetchall()
            for row in rows:
                print(row)
        conn.commit()
#1-Exe
def find_contact(text):
    with get_con() as conn:
        with conn.cursor() as f:
            f.execute("SELECT * FROM find_name_or_phone(%s)",(text, ))
            rows=f.fetchall()
            for row in rows:
                print(f"Name: {row[0]}, Phone: {row[1]}")
#2-Exe
def updsert_user(name,phone):
    with get_con() as conn:
        with conn.cursor() as throw:
            throw.execute("CALL upsert_contact(%s, %s)",(name,phone))
            print("Upserted User")
    conn.commit()
#3_EXE
def add_many_contacts():
    names = ['Dias', 'Maks', 'sergey', 'Aigul','Bagdat']
    phones = ['87071112233', '87014445566', '123', '87470009988','8707aaa1111']
    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM insert_many_users(%s::TEXT[], %s::TEXT[])", (names, phones))
            invalid_data = cur.fetchall()
            conn.commit()
            if invalid_data:
                for row in invalid_data:
                    print(f"name: {row[0]}, phone: {row[1]}")
            else:
                print("Connect all users")
#4_EXE
def see_contact_pages():
    limit=7
    page=int(input("enter your reads page(MAX page=7): "))
    offset=(page-1)*limit
    with get_con() as conn:
        with conn.cursor() as throw:
            throw.execute("SELECT*FROM get_contact_pages(%s,%s)",(limit,offset))
            rows=throw.fetchall()
            if not rows:
                print("This page not information")
            else:
                print(f"-----all information page of{page}-----")
                for row in rows:
                    print(f"name: {row[0]}, phone: {row[1]}")

#5_EXE
def del_contact():
    del_user=input("enter name or phone for delete")
    with get_con() as conn:
        with conn.cursor() as throw:
            throw.execute("CALL delete_contact(%s)",(del_user, ))
        conn.commit()
        print("Delete contact ")
#menu
def menu():
    create_table()
    conn = get_con()
    try:
        execute_Sql_file("functions.sql", conn)
        execute_Sql_file("procedures.sql", conn)
    except:
        pass

    while True:
        print("\n--- MENU ---")
        print("1. Search | 2. Upsert | 3. Add Many | 4. Pages | 5. Delete | 6. see all phonbook practice 8| 0. Exit")
        choice = input("Select: ")
        if choice == '101': find_contact(input("Search term: "))
        elif choice == '202': updsert_user(input("Name: "), input("Phone: "))
        elif choice == '303': add_many_contacts()
        elif choice == '404': see_contact_pages()
        elif choice == '505': del_contact()
        elif choice == '606': see_phonebook_pr8()
        elif choice == '0': break

if __name__ == "__main__":
    menu()