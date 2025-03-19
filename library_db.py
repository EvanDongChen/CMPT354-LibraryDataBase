import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create People table
cursor.execute('''
CREATE TABLE IF NOT EXISTS People (
    PeopleID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Phone TEXT,
    Email TEXT UNIQUE
)
''')

# Create Member table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Member (
    MemberID INTEGER PRIMARY KEY,
    PeopleID INTEGER,
    JoinDate DATE NOT NULL,
    MembershipStatus TEXT CHECK(MembershipStatus IN ('Active', 'Inactive')),
    FOREIGN KEY (PeopleID) REFERENCES People(PeopleID)
)
''')

# Create Employee table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employee (
    EmployeeID INTEGER PRIMARY KEY,
    PeopleID INTEGER,
    Position TEXT NOT NULL,
    WagePerHour REAL NOT NULL,
    FOREIGN KEY (PeopleID) REFERENCES People(PeopleID)
)
''')

# Create Event table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Event (
    EventID INTEGER PRIMARY KEY,
    EventName TEXT NOT NULL,
    Type TEXT NOT NULL,
    EventDate DATETIME NOT NULL
)
''')

# Create AudienceType table
cursor.execute('''
CREATE TABLE IF NOT EXISTS AudienceType (
    AudienceTypeID INTEGER PRIMARY KEY,
    AudienceName TEXT NOT NULL,
    MinAge INTEGER,
    MaxAge INTEGER
)
''')

# Create EventLocation table
cursor.execute('''
CREATE TABLE IF NOT EXISTS EventLocation (
    LocationID INTEGER PRIMARY KEY,
    RoomName TEXT NOT NULL,
    Capacity INTEGER NOT NULL
)
''')

# Create Item table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Item (
    ItemID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Status TEXT CHECK(Status IN ('Available', 'CheckedOut', 'Lost')),
    PublicationYear INTEGER,
    Author TEXT,
    Type TEXT NOT NULL
)
''')

# Create DigitalItem table
cursor.execute('''
CREATE TABLE IF NOT EXISTS DigitalItem (
    ItemID INTEGER PRIMARY KEY,
    URL TEXT NOT NULL,
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
)
''')

# Create PhysicalItem table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PhysicalItem (
    ItemID INTEGER PRIMARY KEY,
    ShelfNumber TEXT NOT NULL,
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
)
''')

# Create ProposedItem table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ProposedItem (
    ProposalID INTEGER PRIMARY KEY,
    ProposalDate DATE NOT NULL,
    IntendedType TEXT CHECK(IntendedType IN ('Digital', 'Physical'))
)
''')

# Create BorrowingTransaction table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BorrowingTransaction (
    TransactionID INTEGER PRIMARY KEY,
    MemberID INTEGER,
    ItemID INTEGER,
    CheckoutDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
)
''')

# Create Fine table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Fine (
    FineID INTEGER PRIMARY KEY,
    TransactionID INTEGER,
    Amount REAL NOT NULL,
    DateReturned DATE,
    PaidDate DATE,
    PaidStatus TEXT CHECK(PaidStatus IN ('Paid', 'Unpaid')),
    FOREIGN KEY (TransactionID) REFERENCES BorrowingTransaction(TransactionID)
)
''')

# Create Requests table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Requests (
    RequestID INTEGER PRIMARY KEY,
    MemberID INTEGER,
    EmployeeID INTEGER,
    Question TEXT NOT NULL,
    Answer TEXT,
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
)
''')

# Create isHeldAt table (Event and EventLocation)
cursor.execute('''
CREATE TABLE IF NOT EXISTS isHeldAt (
    EventID INTEGER,
    LocationID INTEGER,
    PRIMARY KEY (EventID, LocationID),
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (LocationID) REFERENCES EventLocation(LocationID)
)
''')

# Create Recommended table (Event and AudienceType)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Recommended (
    EventID INTEGER,
    AudienceTypeID INTEGER,
    PRIMARY KEY (EventID, AudienceTypeID),
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (AudienceTypeID) REFERENCES AudienceType(AudienceTypeID)
)
''')

# Create Organizes table (Employee and Event)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Organizes (
    EmployeeID INTEGER,
    EventID INTEGER,
    PRIMARY KEY (EmployeeID, EventID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
)
''')

# Create SignUp table (People and Event)
cursor.execute('''
CREATE TABLE IF NOT EXISTS SignUp (
    RegistrationID INTEGER PRIMARY KEY,
    EventID INTEGER,
    PeopleID INTEGER,
    Attended BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (PeopleID) REFERENCES People(PeopleID)
)
''')

# Create isDue table (Fine and BorrowingTransaction)
cursor.execute('''
CREATE TABLE IF NOT EXISTS isDue (
    FineID INTEGER,
    TransactionID INTEGER,
    PRIMARY KEY (FineID, TransactionID),
    FOREIGN KEY (FineID) REFERENCES Fine(FineID),
    FOREIGN KEY (TransactionID) REFERENCES BorrowingTransaction(TransactionID)
)
''')

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all table
tables = cursor.fetchall()

# Print out the table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database schema created successfully")