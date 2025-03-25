import sqlite3

def connect_db():
    conn = sqlite3.connect("library.db")
    conn.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enforced
    return conn

# Function to list all items in the library
'''
def list_all_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Item")
    items = cursor.fetchall()
    conn.close()

    if items:
        print("\nAll Library Items:")
        for item in items:
            print(item)
    else:
        print("No items found in the library.")
'''


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
    
    # Check if the member exists
    cursor.execute("SELECT * FROM Member WHERE MemberID = ?", (member_id,))
    if not cursor.fetchone():
        print("Error: Member does not exist.")
        conn.close()
        return

    # Check item availability
    cursor.execute("SELECT Status FROM Item WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    
    if item and item[0] == "Available":
        cursor.execute("""
            INSERT INTO BorrowingTransaction (MemberID, ItemID, CheckoutDate, DueDate)
            VALUES (?, ?, DATE('now'), DATE('now', '+14 days'))
        """, (member_id, item_id))

        # Update status to 'CheckedOut'
        cursor.execute("UPDATE Item SET Status = 'CheckedOut' WHERE ItemID = ?", (item_id,))
        conn.commit()
        print("Item borrowed successfully!")
    else:
        print("Item is not available.")
    
    conn.close()

# Function to return an item
def return_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if the item exists
    cursor.execute("SELECT Status FROM Item WHERE ItemID = ?", (item_id,))
    if not cursor.fetchone():
        print("Error: Item does not exist.")
        conn.close()
        return

    # Set the item status back to Available
    cursor.execute("UPDATE Item SET Status = 'Available' WHERE ItemID = ?", (item_id,))
        
    # Update transaction with return date
    cursor.execute("""
        UPDATE BorrowingTransaction 
        SET ReturnDate = DATE('now') 
        WHERE ItemID = ? AND ReturnDate IS NULL
    """, (item_id,))
    
    conn.commit()
    print("Item returned successfully!")
    conn.close()

# Function to donate an item
def donate_item(title, author, publication_year, item_type):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Item (Title, Author, PublicationYear, Type, Status)
            VALUES (?, ?, ?, ?, 'Available')
        """, (title, author, publication_year, item_type))
        conn.commit()
        print("Item donated successfully!")
    except sqlite3.IntegrityError:
        print("Error: Could not donate item.")
    conn.close()

# Function to find events in the library
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
    
    # Validate if user exists
    cursor.execute("SELECT * FROM People WHERE PeopleID = ?", (user_id,))
    if not cursor.fetchone():
        print("Error: User does not exist.")
        conn.close()
        return
    
    try:
        cursor.execute("INSERT INTO SignUp (EventID, PeopleID) VALUES (?, ?)", (event_id, user_id))
        conn.commit()
        print("Registered for event successfully!")
    except sqlite3.IntegrityError:
        print("Error: Could not register for the event.")
    
    conn.close()

# Function to ask for librarian help
def ask_librarian(user_id, question):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Validate member exists
    cursor.execute("SELECT * FROM Member WHERE MemberID = ?", (user_id,))
    if not cursor.fetchone():
        print("Error: Member does not exist.")
        conn.close()
        return
    
    try:
        cursor.execute("INSERT INTO Requests (MemberID, Question) VALUES (?, ?)", (user_id, question))
        conn.commit()
        print("Librarian request submitted!")
    except sqlite3.IntegrityError:
        print("Error: Could not submit librarian request.")
    
    conn.close()

def main():
    while True:
        print("\nLibrary Database Menu:")
        print("1. Find an item")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event")
        print("7. Ask for librarian help")
        print("8. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter item title: ")
            items = find_item(title)
            if items:
                for item in items:
                    print(item)
            else:
                print("No items found.")
        
        elif choice == "2":
            member_id = input("Enter your Member ID: ")
            item_id = input("Enter Item ID: ")
            if member_id.isdigit() and item_id.isdigit():
                borrow_item(int(member_id), int(item_id))
            else:
                print("Invalid input. Please enter valid IDs.")
        
        elif choice == "3":
            item_id = input("Enter Item ID to return: ")
            if item_id.isdigit():
                return_item(int(item_id))
            else:
                print("Invalid input. Please enter a valid ID.")
        
        elif choice == "4":
            title = input("Enter title: ")
            author = input("Enter author: ")
            publication_year = input("Enter publication year: ")
            item_type = input("Enter item type (Digital/Physical): ")
            if publication_year.isdigit():
                donate_item(title, author, int(publication_year), item_type)
            else:
                print("Invalid year. Please enter a numeric value.")
        
        elif choice == "5":
            event_name = input("Enter event name: ")
            events = find_event(event_name)
            if events:
                for event in events:
                    print(event)
            else:
                print("No events found.")
        
        elif choice == "6":
            user_id = input("Enter your Member ID: ")
            event_id = input("Enter Event ID: ")
            if user_id.isdigit() and event_id.isdigit():
                register_event(int(user_id), int(event_id))
            else:
                print("Invalid input. Please enter valid IDs.")
        
        elif choice == "7":
            user_id = input("Enter your Member ID: ")
            question = input("Enter your question for the librarian: ")
            if user_id.isdigit():
                ask_librarian(int(user_id), question)
            else:
                print("Invalid input. Please enter a valid Member ID.")
        
        elif choice == "8":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
