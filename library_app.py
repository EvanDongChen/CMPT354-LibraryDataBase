import sqlite3

def connect_db():
    return sqlite3.connect("library.db")
# Function to find an item in the library
def find_item(title):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Item WHERE Title LIKE ?", (f"%{title}%",))
    items = cursor.fetchall()
    conn.close()
    return items

# Function to borrow an item
def borrow_item(member_id, item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Status FROM Item WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    
    if item and item[0] == "Available":
        cursor.execute("INSERT INTO BorrowingTransaction (MemberID, ItemID, CheckoutDate, DueDate) VALUES (?, ?, DATE('now'), DATE('now', '+14 days'))", (member_id, item_id))
        cursor.execute("UPDATE Item SET Status = 'Borrowed' WHERE ItemID = ?", (item_id,))
        conn.commit()
        print("Item borrowed successfully!")
    else:
        print("Item is not available.")
    conn.close()

# Function to return an item
def return_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Item SET Status = 'Available' WHERE ItemID = ?", (item_id,))
    cursor.execute("UPDATE BorrowingTransaction SET ReturnDate = DATE('now') WHERE ItemID = ? AND ReturnDate IS NULL", (item_id,))
    conn.commit()
    print("Item returned successfully!")
    conn.close()

# Function to donate an item
def donate_item(title, author, publication_year, item_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Item (Title, Author, PublicationYear, Type, Status) VALUES (?, ?, ?, ?, 'Available')", (title, author, publication_year, item_type))
    conn.commit()
    print("Item donated successfully!")
    conn.close()

# Function to find events
def find_event(event_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Event WHERE EventName LIKE ?", (f"%{event_name}%",))
    events = cursor.fetchall()
    conn.close()
    return events

# Function to register for an event
def register_event(user_id, event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO EventRegistrations (UserID, EventID) VALUES (?, ?)", (user_id, event_id))
    conn.commit()
    print("Registered for event successfully!")
    conn.close()

# Function to volunteer
def volunteer(user_id, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Volunteers (UserID, Role) VALUES (?, ?)", (user_id, role))
    conn.commit()
    print("Volunteer registration successful!")
    conn.close()

# Function to ask for librarian help
def ask_librarian(user_id, question):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO LibrarianRequests (UserID, Question, RequestDate) VALUES (?, ?, DATE('now'))", (user_id, question))
    conn.commit()
    print("Librarian request submitted!")
    conn.close()



def main():
    
    while True:
        print("\nLibrary Menu:")
        print("1. Find an item")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event")
        print("7. Volunteer for the library")
        print("8. Ask for librarian help")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter item title: ")
            print(find_item(title))
        elif choice == "2":
            member_id = int(input("Enter your Member ID: "))
            item_id = int(input("Enter Item ID: "))
            borrow_item(member_id, item_id)
        elif choice == "3":
            item_id = int(input("Enter Item ID to return: "))
            return_item(item_id)
        elif choice == "4":
            title = input("Enter title: ")
            author = input("Enter author: ")
            publication_year = input("Enter publication year: ")
            item_type = input("Enter item type (Digital/Physical): ")
            donate_item(title, author, publication_year, item_type)
        elif choice == "5":
            event_name = input("Enter event name: ")
            print(find_event(event_name))
        elif choice == "6":
            user_id = int(input("Enter your User ID: "))
            event_id = int(input("Enter Event ID: "))
            register_event(user_id, event_id)
        elif choice == "7":
            user_id = int(input("Enter your User ID: "))
            role = input("Enter role you want to volunteer for: ")
            volunteer(user_id, role)
        elif choice == "8":
            user_id = int(input("Enter your User ID: "))
            question = input("Enter your question for the librarian: ")
            ask_librarian(user_id, question)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
