import sqlite3

def clear_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Disable foreign key constraints to avoid issues while deleting
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # List of tables to clear
    tables = [
        "People", "Member", "Employee", "Event", "Item", "BorrowingTransaction",
        "Fine", "Requests", "isHeldAt", "Recommended", "Organizes", "SignUp",
        "isDue", "DigitalItem", "PhysicalItem", "ProposedItem", "AudienceType",
        "EventLocation"
    ]

    # Delete data from all tables
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
    
    # Re-enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    conn.commit()
    conn.close()
    print("Database cleared.")

def populate_data():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Insert people
    cursor.executemany("""
        INSERT INTO People (PeopleID, FirstName, LastName, Phone, Email)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "Alice", "Smith", "123-456-7890", "alice@example.com"),
        (2, "Bob", "Johnson", "987-654-3210", "bob@example.com"),
        (3, "Charlie", "Brown", "555-666-7777", "charlie@example.com"),
    ])

    # Insert members
    cursor.executemany("""
        INSERT INTO Member (MemberID, PeopleID, JoinDate, MembershipStatus)
        VALUES (?, ?, ?, ?)
    """, [
        (1, 1, "2024-01-10", "Active"),
        (2, 2, "2024-02-15", "Active"),
    ])

    # Insert employee (librarian)
    cursor.execute("""
        INSERT INTO Employee (EmployeeID, PeopleID, Position, WagePerHour)
        VALUES (?, ?, ?, ?)
    """, (1, 3, "Librarian", 25.00))

    # Insert books
    cursor.executemany("""
        INSERT INTO Item (ItemID, Title, Status, PublicationYear, Author, Type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        (1, "Book One", "Available", 2020, "Author A", "Physical"),
        (2, "Book Two", "Available", 2018, "Author B", "Physical"),
        (3, "Book Three", "CheckedOut", 2015, "Author C", "Physical"),
    ])

    # Insert events
    cursor.executemany("""
        INSERT INTO Event (EventID, EventName, Type, EventDate)
        VALUES (?, ?, ?, ?)
    """, [
        (1, "Book Club", "Reading", "2024-03-25 18:00:00"),
        (2, "Author Talk", "Discussion", "2024-04-10 15:00:00"),
    ])

    conn.commit()
    conn.close()
    print("Database populated.")

if __name__ == "__main__":
     # First, clear existing data
    clear_database()
     # Then, insert new records 
    populate_data()  
