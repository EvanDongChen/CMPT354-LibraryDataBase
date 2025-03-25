from app import create_app, db
from app.models import (
    People, Member, Employee, Event, AudienceType, EventLocation,
    Item, DigitalItem, PhysicalItem, ProposedItem, BorrowingTransaction,
    Fine, Request, IsHeldAt, Recommended, Organizes, SignUp, IsDue
)

# Create app and context
app = create_app()
app.app_context().push()

def clear_database():
    """Clear all database tables"""
    # Disable foreign key constraints
    db.session.execute('PRAGMA foreign_keys=OFF;')
    
    # Get all table names in correct deletion order
    tables = [
        'is_due', 'fine', 'borrowing_transaction', 'sign_up', 'organizes',
        'recommended', 'is_held_at', 'request', 'physical_item', 'digital_item',
        'item', 'proposed_item', 'employee', 'member', 'event', 'audience_type',
        'event_location', 'people'
    ]
    
    for table in tables:
        db.session.execute(f'DELETE FROM {table};')
    
    # Re-enable foreign key constraints
    db.session.execute('PRAGMA foreign_keys=ON;')
    db.session.commit()
    print("Database cleared.")

def populate_data():
    """Populate database with sample data"""
    # Add People
    people_data = [
        People(PeopleID=1, FirstName="Alice", LastName="Smith", Phone="123-456-7890", Email="alice@example.com"),
        People(PeopleID=2, FirstName="Bob", LastName="Johnson", Phone="987-654-3210", Email="bob@example.com"),
        People(PeopleID=3, FirstName="Charlie", LastName="Brown", Phone="555-666-7777", Email="charlie@example.com"),
        People(PeopleID=4, FirstName="Diana", LastName="Miller", Phone="111-222-3333", Email="diana@example.com"),
    ]
    db.session.add_all(people_data)

    # Add Members
    member_data = [
        Member(MemberID=1, PeopleID=1, JoinDate=datetime(2024, 1, 10), MembershipStatus="Active"),
        Member(MemberID=2, PeopleID=2, JoinDate=datetime(2024, 2, 15), MembershipStatus="Active"),
    ]
    db.session.add_all(member_data)

    # Add Employees
    employee_data = [
        Employee(EmployeeID=1, PeopleID=3, Position="Librarian", WagePerHour=25.00),
        Employee(EmployeeID=2, PeopleID=4, Position="Assistant Librarian", WagePerHour=20.00),
    ]
    db.session.add_all(employee_data)

    # Add Event Locations
    locations = [
        EventLocation(LocationID=1, RoomName="Main Hall", Capacity=100),
        EventLocation(LocationID=2, RoomName="Conference Room", Capacity=30),
    ]
    db.session.add_all(locations)

    # Add Audience Types
    audiences = [
        AudienceType(AudienceTypeID=1, AudienceName="Children", MinAge=5, MaxAge=12),
        AudienceType(AudienceTypeID=2, AudienceName="Adults", MinAge=18),
    ]
    db.session.add_all(audiences)

    # Add Events
    events = [
        Event(EventID=1, EventName="Story Time", Type="Reading", EventDate=datetime(2024, 3, 25, 10, 0)),
        Event(EventID=2, EventName="Author Talk", Type="Discussion", EventDate=datetime(2024, 4, 10, 18, 0)),
    ]
    db.session.add_all(events)

    # Add Event Locations (IsHeldAt)
    held_at = [
        IsHeldAt(EventID=1, LocationID=1),
        IsHeldAt(EventID=2, LocationID=2),
    ]
    db.session.add_all(held_at)

    # Add Event Audiences (Recommended)
    recommendations = [
        Recommended(EventID=1, AudienceTypeID=1),
        Recommended(EventID=2, AudienceTypeID=2),
    ]
    db.session.add_all(recommendations)

    # Add Event Organizers (Organizes)
    organizers = [
        Organizes(EmployeeID=1, EventID=1),
        Organizes(EmployeeID=2, EventID=2),
    ]
    db.session.add_all(organizers)

    # Add Items
    items = [
        Item(ItemID=1, Title="The Great Adventure", Status="Available", PublicationYear=2020, Author="Author A", Type="Physical"),
        Item(ItemID=2, Title="Digital World", Status="Available", PublicationYear=2021, Author="Author B", Type="Digital"),
        Item(ItemID=3, Title="Science Today", Status="CheckedOut", PublicationYear=2019, Author="Author C", Type="Physical"),
    ]
    db.session.add_all(items)

    # Add Physical Items
    physical_items = [
        PhysicalItem(ItemID=1, ShelfNumber="A101"),
        PhysicalItem(ItemID=3, ShelfNumber="B205"),
    ]
    db.session.add_all(physical_items)

    # Add Digital Items
    digital_items = [
        DigitalItem(ItemID=2, URL="https://example.com/digital-world"),
    ]
    db.session.add_all(digital_items)

    # Add Proposed Items
    proposed_items = [
        ProposedItem(ProposalID=1, ProposalDate=datetime(2024, 3, 1), IntendedType="Physical", Title="New Science Book", Author="New Author"),
    ]
    db.session.add_all(proposed_items)

    # Add Borrowing Transactions
    transactions = [
        BorrowingTransaction(
            TransactionID=1,
            MemberID=1,
            ItemID=3,
            CheckoutDate=datetime(2024, 3, 1),
            DueDate=datetime(2024, 3, 15),
            ReturnDate=None
        ),
    ]
    db.session.add_all(transactions)

    # Add Fines
    fines = [
        Fine(
            FineID=1,
            TransactionID=1,
            Amount=5.00,
            DateReturned=None,
            PaidDate=None,
            PaidStatus=False
        ),
    ]
    db.session.add_all(fines)

    # Add IsDue relationships
    is_due = [
        IsDue(FineID=1, TransactionID=1),
    ]
    db.session.add_all(is_due)

    # Add Requests
    requests = [
        Request(
            RequestID=1,
            PeopleID=1,
            Question="Do you have more books by this author?",
            Answer="Yes, we'll order more titles."
        ),
    ]
    db.session.add_all(requests)

    # Add Event Signups
    signups = [
        SignUp(RegistrationID=1, EventID=1, PeopleID=1, Attended=False),
        SignUp(RegistrationID=2, EventID=2, PeopleID=2, Attended=False),
    ]
    db.session.add_all(signups)

    db.session.commit()
    print("Database populated with sample data.")

if __name__ == "__main__":
    clear_database()
    populate_data()