# phonebook.py
import csv
import psycopg2
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute("INSERT INTO contacts (username, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (username, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET phone=%s WHERE username=%s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()

def query_contacts():
    prefix = input("Enter phone prefix: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (prefix + "%",))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_contact():
    name = input("Enter name to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE username=%s", (name,))
    conn.commit()
    cur.close()
    conn.close()

def menu():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break

if __name__ == "__main__":
    menu()
