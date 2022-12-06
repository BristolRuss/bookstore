import sqlite3
from tabulate import tabulate

def create_database(books):
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)");
        cursor.executemany("INSERT OR IGNORE INTO books(id, title, author, qty) VALUES (:id, :title, :author, :qty)", books)
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()

def display_all():
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        cursor.execute("SELECT id, title, author, qty FROM books")
        print(f"\n{'-' * 30} View All {'-' * 30}")
        print(tabulate(cursor.fetchall(), headers=["id", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()

menu_choices = [
    [1, "Add Book"],
    [2, "Update Book"],
    [3, "Delete Book"],
    [4, "Search Book"],
    [5, "View All Books"],
    [6, "Exit"]
]

initial_books = [{'id': 3001, 'title': 'A Tale of Two Cities', 'author': 'Charles Dickens', 'qty': 30}, {'id': 3002, 'title': 'Harry Potter and the Philosopher\'s Stone', 'author': 'J.K. Rowling', 'qty': 40}, {'id': 3003, 'title': 'The Lion, the Witch and the Wardrobe', 'author': 'C.S. Lewis', 'qty': 25}, {'id': 3004, 'title': 'The Lord of the Rings', 'author': 'J.R.R Tolkien', 'qty': 37}, {'id': 3005, 'title': 'Alice in Wonderland', 'author': 'Lewis Carroll', 'qty': 12}]

while True:
    create_database(initial_books)
    print("\n--------- Main Menu ---------")
    print(tabulate(menu_choices, headers=["Option", "Function"], tablefmt="rounded_grid"))
    while True:
        try:
            user_selection = int(input("Please Select An Option: "))
            if user_selection > 0 and user_selection <= len(menu_choices):
                break
            else:
                print("Sorry, that was not a valid option. Please try again.")
        except ValueError:
            print("Sorry, that input was not valid. Please try again.")
    if user_selection == 5:
        display_all()
    if user_selection == 6:
        exit()