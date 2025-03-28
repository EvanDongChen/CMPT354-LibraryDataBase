import sys
import os
from datetime import datetime

# Ensure backend is on the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app import create_app, db
from app.models import (
    People, Member, Employee, Event, AudienceType, EventLocation,
    Item, DigitalItem, PhysicalItem, ProposedItem, BorrowingTransaction,
    Fine, Request, IsHeldAt, Recommended, Organizes, SignUp, IsDue
)

# Create app and push context
app = create_app()
app.app_context().push()

def clear_database():
    db.reflect()
    db.drop_all()
    db.create_all()
    print("✅ Database reset complete")

def populate_data():
    # Add People
    people_data = [
        People(PeopleID=1, FirstName="Alice", LastName="Smith", Phone="123-456-7890", Email="alice@example.com"),
        People(PeopleID=2, FirstName="Bob", LastName="Johnson", Phone="987-654-3210", Email="bob@example.com"),
        People(PeopleID=3, FirstName="Charlie", LastName="Brown", Phone="555-666-7777", Email="charlie@example.com"),
        People(PeopleID=4, FirstName="Diana", LastName="Miller", Phone="111-222-3333", Email="diana@example.com"),
    ]
    db.session.add_all(people_data)

    member_data = [
        Member(MemberID=1, PeopleID=1, JoinDate=datetime(2024, 1, 10), MembershipStatus="Active"),
        Member(MemberID=2, PeopleID=2, JoinDate=datetime(2024, 2, 15), MembershipStatus="Active"),
    ]
    db.session.add_all(member_data)

    employee_data = [
        Employee(EmployeeID=1, PeopleID=3, Position="Librarian", WagePerHour=25.00),
        Employee(EmployeeID=2, PeopleID=4, Position="Assistant Librarian", WagePerHour=20.00),
    ]
    db.session.add_all(employee_data)

    locations = [
        EventLocation(LocationID=1, RoomName="Main Hall", Capacity=100),
        EventLocation(LocationID=2, RoomName="Conference Room", Capacity=30),
    ]
    db.session.add_all(locations)

    audiences = [
        AudienceType(AudienceTypeID=1, AudienceName="Children", MinAge=5, MaxAge=12),
        AudienceType(AudienceTypeID=2, AudienceName="Adults", MinAge=18),
    ]
    db.session.add_all(audiences)

    events = [
        Event(EventID=1, EventName="Story Time", Type="Reading", EventDate=datetime(2024, 3, 25, 10, 0)),
        Event(EventID=2, EventName="Author Talk", Type="Discussion", EventDate=datetime(2024, 4, 10, 18, 0)),
    ]
    db.session.add_all(events)

    db.session.add_all([
        IsHeldAt(EventID=1, LocationID=1),
        IsHeldAt(EventID=2, LocationID=2),
    ])

    db.session.add_all([
        Recommended(EventID=1, AudienceTypeID=1),
        Recommended(EventID=2, AudienceTypeID=2),
    ])

    db.session.add_all([
        Organizes(EmployeeID=1, EventID=1),
        Organizes(EmployeeID=2, EventID=2),
    ])

    items = [
        Item(ItemID=1, Title="The Great Adventure", Status="Available", PublicationYear=2020, Author="Author A", Type="Book"),
        Item(ItemID=2, Title="Digital World", Status="Available", PublicationYear=2021, Author="Author B", Type="Book"),
        Item(ItemID=3, Title="Science Today", Status="CheckedOut", PublicationYear=2019, Author="Author C", Type="Magazine"),
        Item(ItemID=4, Title="Nature Journal", Status="Available", PublicationYear=2022, Author="Various", Type="Scientific Journal"),
        Item(ItemID=5, Title="Classical Collection", Status="Available", PublicationYear=2020, Author="Various Artists", Type="CD"),
        Item(ItemID=6, Title="Jazz Classics", Status="Available", PublicationYear=1960, Author="Various Artists", Type="Record"),
    ]
    db.session.add_all(items)

    db.session.add_all([
        PhysicalItem(ItemID=1, ShelfNumber="A101"),  # Book
        PhysicalItem(ItemID=3, ShelfNumber="B205"),  # Magazine
        PhysicalItem(ItemID=5, ShelfNumber="C303"),  # CD
        PhysicalItem(ItemID=6, ShelfNumber="D404"),  # Record
    ])

    db.session.add_all([
        DigitalItem(ItemID=2, URL="https://example.com/digital-world"),  # Digital Book
        DigitalItem(ItemID=4, URL="https://example.com/nature-journal"),  # Digital Journal
    ])

    db.session.add_all([
        ProposedItem(ProposalID=1, ProposalDate=datetime(2024, 3, 1), IntendedType="Physical", Title="New Science Book", Author="New Author"),
    ])

    db.session.add_all([
        BorrowingTransaction(TransactionID=1, MemberID=1, ItemID=3, CheckoutDate=datetime(2024, 3, 1), DueDate=datetime(2024, 3, 15), ReturnDate=None),
    ])

    db.session.add_all([
        Fine(FineID=1, TransactionID=1, Amount=5.00, DateReturned=None, PaidDate=None, PaidStatus=False),
        IsDue(FineID=1, TransactionID=1),
    ])

    db.session.add_all([
        Request(RequestID=1, PeopleID=1, Question="Do you have more books by this author?", Answer="Yes, we'll order more titles."),
    ])

    db.session.add_all([
        SignUp(RegistrationID=1, EventID=1, PeopleID=1, Attended=False),
        SignUp(RegistrationID=2, EventID=2, PeopleID=2, Attended=False),
    ])

    db.session.commit()
    print("✅ Database populated with sample data.")

if __name__ == "__main__":
    clear_database()
    populate_data()
