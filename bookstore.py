# we import the sqlite and tabulate modules
import sqlite3
from tabulate import tabulate

# we create a function which connects to a database (which it creates if it doesn't yet exist), creates our book table and inserts our starting data using sqlite
def create_database(books):
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        # we use 'IF NOT EXISTS' so that if the table already exists this code will skip
        cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)");
        # we use 'OR IGNORE' so if the rows already exist this code will skip
        cursor.executemany("INSERT OR IGNORE INTO books(id, title, author, qty) VALUES (:id, :title, :author, :qty)", books)
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()

# we create a function called search_database which takes two arguments, the first is what fields to search, and the second is the search criteria
def search_database(search_fields, search_data):
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        cursor.execute(f"SELECT {search_fields} FROM books {search_data}")
        # once we have our search results we return this information
        return cursor.fetchall()
    except Exception as error:
        db.rollback()
    finally:
        db.close()

# we create a function called update_database which takes three arguments, the field to update, the new data, and the ID of the record we will be updating
def update_database(field, data, id):
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        # we updated the database using the variables passed into the function
        cursor.execute(f"UPDATE books SET {field} = '{data}' WHERE id = '{id}'")
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()
        # once we finish we print a message stating that the record has been updated successfully
        print('''
****************
* Book Updated *
****************''')

# we create a function called delete_from_database which takes an id as an argument. 
def delete_from_database(id):
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        # we delete a record from the table using the id passed into the function as a variable
        cursor.execute(f"DELETE FROM books WHERE id = '{id}'")
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()
        # once we finish we print a message stating that the record has been deleted successfully
        print('''
****************
* Book Deleted *
****************''')

# we create a function which creates a pause. We use this after we have displayed search results to the user so they have time to analyse the results
def pause_for_input():
    input("Press Enter to continue...")

# we create a function which gets the ID of every entry in the database and assigns the results to a list which we return
def get_id_list():
    id_list = search_database('id', '')
    for index, value in enumerate(id_list):
        id_list[index] = value[0]
    return id_list

# we create a function which adds a new book to the database
def add_book():
    new_title = input("Please enter the title of the book: ")
    new_author = input("Please enter the author of the book: ")
    # we check if a book with the new title AND new author already exists in the database
    already_exists = search_database("*", f"WHERE title = '{new_title}' AND author = '{new_author}'")
    # if a book with the same details already exists we ask the user if they still wish to go ahead
    if already_exists != None and len(already_exists) >= 1:
        while True:
            print(tabulate(already_exists, headers=["ID", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
            cancel_or_not = input("The above book(s) already exists, do you still want to add this book? Enter Y/N: ")
            if cancel_or_not.lower() == "n":
                main_menu()
            elif cancel_or_not.lower() == "y":
                break
            else:
                print("Sorry, you need to enter Y or N")
    while True:
        try:
            new_qty = int(input("Please enter the quantity of the book: "))
            break
        except ValueError:
            print("Sorry, the quantity needs to be a number. Please try again.")
    # once we have all of the new book information we add it to the database
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        cursor.execute("INSERT INTO books(title, author, qty) VALUES (?, ?, ?)", (new_title, new_author, new_qty))
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()
        # finally we print a message to the user that their book was added successfully
        print('''
**************
* Book Added *
**************''')

# we create a function which searches the database and returns results based on user criteria
def search_book():
    while True:
        try:
            print(tabulate([["1", "ID"], ["2", "Title"], ["3", "Author"], ["4", "Quantity"], ["5", "Return To Main Menu"]], headers=["Option", "Selection"], tablefmt="rounded_grid"))
            user_selection = int(input("What criteria would you like to search on?: "))
            if user_selection > 0 and user_selection <= 5:
                break
            else:
                print("Sorry, that value was in range. Please try again")
        except ValueError:
            print("Sorry, that selection was not valid. Please try again.")
    # we search the database for a record matching the ID that the user enters
    if user_selection == 1:
        while True:
            try:
                id_search = int(input("Please enter the ID number you would like to search for. Enter -1 to return to main menu: "))
                if id_search == -1:
                    main_menu()
                results = search_database("*", f"WHERE id = {id_search}")
                if results != None and len(results) >= 1:
                    print("\n------------ Results -------------")
                    print(tabulate(results, headers=["ID", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
                    return results
                else:
                    print("\nSorry, no matching records found")
            except ValueError:
                print("Sorry, the ID number must be a number. Please try again.")
    # we search the database for records matching the title that the user enters
    elif user_selection == 2:
        title_search = input("Please enter the name of the title you are searching for. Enter -1 to return to main menu: ")
        if title_search == "-1":
            main_menu()
        results = search_database("*", f"WHERE title LIKE '{title_search}'")
        if results != None and len(results) >= 1:
            print("\n------------ Results -------------")
            print(tabulate(results, headers=["ID", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
            return results
        else:
            print("\nSorry, no matching records found")
    # we search the database for entries matching the author that the user enters
    elif user_selection == 3:
        author_search = input("Please enter the name of the author you are searching for. Enter -1 to return to main menu: ")
        if author_search == "-1":
            main_menu()
        results = search_database("*", f"WHERE author LIKE '{author_search}'")
        if results != None and len(results) >= 1:
            print("\n------------ Results -------------")
            print(tabulate(results, headers=["ID", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
            return results
        else:
            print("\nSorry, no matching records found")
    # we search the database for entries matching the quantity that the user enters
    elif user_selection == 4:
        while True:
            try:
                print("\n----- Quantity Search -----\n")
                # we display what operators the user has available to them
                print(tabulate([["=","<", ">", "<=", ">=", "!="]], tablefmt="rounded_grid"))
                qty_search = input("Please enter your search criteria with an operator from the list above. Enter -1 to return to main menu: ")
                if qty_search == -1:
                    main_menu()
                results = search_database("*", f"WHERE qty {qty_search}")
                if results != None and len(results) >= 1:
                    print("\n------------ Results -------------")
                    print(tabulate(results, headers=["ID", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
                    return results
                else:
                    print("\nSorry, no matching records found")
            except ValueError:
                print("Sorry, the quantity must be a number. Please try again.")
    elif user_selection == 5:
        main_menu()

# we create a function which searches for a book to update in the database
def update_book():
    while True:
        print("\n------------ Update Book ------------")
        # we use our search_book function to search the database
        search_results = search_book()
        if search_results != None and len(search_results) > 1:
            while True:
                try:
                    id_list = []
                    for index, value in enumerate(search_results):
                        id_list.append(value[0])
                    # if the users search returns results we ask the user to enter the ID of the record they would like to edit
                    select_id = int(input("Please enter the ID of the book you would like to edit. Enter -1 to return to main menu: "))
                    if select_id == -1:
                        main_menu()
                    elif select_id in id_list:
                        # we pass the user selected ID to our edit_book function
                        edit_book(select_id)
                        break
                    else:
                        print("Sorry, that ID number was not in the list")
                except ValueError:
                    print("Sorry, the ID must be a number.")
            break
        elif search_results != None and len(search_results) == 1:
            # if only one result is returned we pass this result straight to our edit_book function
            edit_book(search_results[0][0])
            break

# we create a function called edit_book which takes an ID as an argument
def edit_book(id):
    while True:
        print("\n ----------- Edit Book -----------\n")
        # we print the options available to the user
        print(tabulate([["1", "Title"], ["2", "Author"], ["3", "Quantity"], ["4", "Return To Main Menu"]], headers=["Option", "Selection"], tablefmt="rounded_grid"))
        try:
            # we ask the user to enter an option and then run that selection
            user_selection = int(input("Please enter what field you would like to edit. Enter -1 to return to main menu: "))
            if user_selection == 4:
                main_menu()
            elif user_selection == 1:
                new_title = input("Please enter the new title: ")
                # once the user has entered the new title we pass this to our update_database function
                update_database("title", new_title, id)
                break
            elif user_selection == 2:
                new_author = input("Please enter the new author: ")
                # once the user has entered the new author we pass this to our update_database function
                update_database('author', new_author, id)
                break
            elif user_selection == 3:
                while True:
                    try:
                        new_qty = int(input("Please enter the new quantity: "))
                        # once the user has entered the new quantity we pass this to our update_database function
                        update_database('qty', new_qty, id)
                        break
                    except ValueError:
                        print("Sorry, the quantity must be a number. Please try again")
                break
            else:
                print("Sorry, that selection was not valid.")
        except ValueError:
            print("Sorry, that selection was not valid")

# we create a function which searches for a record to delete from the database
def delete_book():
    # we run our search_book function to allow the user to filter the results in order to find the record they want to delete
    search_book()
    while True:
        try:
            # once the user has the results we ask them to enter the ID of the record they wish to delete
            user_selection = int(input("Please enter the ID of the book you would like to delete. Enter -1 at anytime to return to main menu: "))
            if user_selection == -1:
                main_menu()
            # we check that the ID the user has entered is valid using our get_id_list function
            elif user_selection in get_id_list():
                try:
                    # we ask the user to confirm the ID of the record they wish to delete
                    confirmation = int(input("Please confirm you want to delete by entering the ID again: "))
                    if confirmation == -1:
                        main_menu()
                    # we check that the confirmation matches the ID the user originally enters and if it does we pass that ID to our delete_from_database function
                    elif confirmation == user_selection:
                        delete_from_database(user_selection)
                        break
                    else:
                        # if the confirmation didn't match we return the user to the start of the function
                        print("Sorry, the confirmation did not match.")
                        pause_for_input()
                        delete_book()
                        break
                except ValueError:
                    print("Sorry, that input was not valid. Please try again")
            else:
                print("Sorry, that ID is not in the list")
        except ValueError:
            print("Sorry, that input was not valid. Please try again.")

# we create a function which searches the database for all entries and then prints the result out to the user
def display_all():
    try:
        db = sqlite3.connect('ebookstore')
        cursor = db.cursor()
        cursor.execute("SELECT id, title, author, qty FROM books")
        print(tabulate(cursor.fetchall(), headers=["id", "Title", "Author", "Quantity"], tablefmt="rounded_grid"))
    except Exception as error:
        db.rollback()
        raise error
    finally:
        db.close()

# we create a function which acts as our main menu
def main_menu():
    while True:
        print(logo)
        print(tabulate(menu_choices, headers=["Option", "Function"], tablefmt="rounded_grid"))
        # we ask the user to select an option and then run the appropriate task
        while True:
            try:
                user_selection = int(input("Please Select An Option: "))
                if user_selection > 0 and user_selection <= len(menu_choices):
                    break
                else:
                    print("Sorry, that was not a valid option. Please try again.")
            except ValueError:
                print("Sorry, that input was not valid. Please try again.")
        if user_selection == 1:
            add_book()
            # once a book has been added we ask if they would like to enter another
            while True:
                selection = input("\nWould you like to add another book? Y/N: ")
                if selection.lower() == "y":
                    add_book()
                elif selection.lower() == "n":
                    break
                else:
                    print("Sorry, that selection was not valid")
        elif user_selection == 2:
            update_book()
        elif user_selection == 3:
            print(f"\n{'-' * 10} Delete Book {'-' * 10}")
            delete_book()
        elif user_selection == 4:
            print("\n---------- Search Book ----------")
            search_book()
            # once the user has finished searching for a book we ask if they would like to run another search
            while True:
                selection = input("Would you like to search for another book? Y/N: ")
                if selection.lower() == "y":
                    search_book()
                elif selection.lower() == "n":
                    break
                else:
                    print("Sorry, that selection was not valid")
        elif user_selection == 5:
            print(f"\n{'-' * 30} View All {'-' * 30}")
            display_all()
            # once the results have been printed we use our pause_for_input function to allow the user to study the information before being returned to the main menu
            pause_for_input()
        elif user_selection == 6:
            exit()

# we create a list which contains our options for our main menu
menu_choices = [
    [1, "Add Book"],
    [2, "Update Book"],
    [3, "Delete Book"],
    [4, "Search Book"],
    [5, "View All Books"],
    [6, "Exit"]
]

# we create a list which contains our initial database entries
initial_books = [{'id': 3001, 'title': 'A Tale of Two Cities', 'author': 'Charles Dickens', 'qty': 30}, {'id': 3002, 'title': 'Harry Potter and the Philosopher\'s Stone', 'author': 'J.K. Rowling', 'qty': 40}, {'id': 3003, 'title': 'The Lion, the Witch and the Wardrobe', 'author': 'C.S. Lewis', 'qty': 25}, {'id': 3004, 'title': 'The Lord of the Rings', 'author': 'J.R.R Tolkien', 'qty': 37}, {'id': 3005, 'title': 'Alice in Wonderland', 'author': 'Lewis Carroll', 'qty': 12}]

# an ascii logo we use on our main menu
logo = '''
$$$$$$$\                   $$\              $$$$$$\   $$\                                
$$  __$$\                  $$ |            $$  __$$\  $$ |                               
$$ |  $$ |$$$$$$\  $$$$$$\ $$ |  $$\       $$ /  \__$$$$$$\   $$$$$$\  $$$$$$\  $$$$$$\  
$$$$$$$\ $$  __$$\$$  __$$\$$ | $$  |      \$$$$$$\ \_$$  _| $$  __$$\$$  __$$\$$  __$$\ 
$$  __$$\$$ /  $$ $$ /  $$ $$$$$$  /        \____$$\  $$ |   $$ /  $$ $$ |  \__$$$$$$$$ |
$$ |  $$ $$ |  $$ $$ |  $$ $$  _$$<        $$\   $$ | $$ |$$\$$ |  $$ $$ |     $$   ____|
$$$$$$$  \$$$$$$  \$$$$$$  $$ | \$$\       \$$$$$$  | \$$$$  \$$$$$$  $$ |     \$$$$$$$\ 
\_______/ \______/ \______/\__|  \__|       \______/   \____/ \______/\__|      \_______|'''

# on program launch this is the first thing that will run. This will initialise our database and tables if not already done so
create_database(initial_books)
# after our database has been initialised we run our main menu function
main_menu()