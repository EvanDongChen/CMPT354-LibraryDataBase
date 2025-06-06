from app.extensions import db
from datetime import datetime

class People(db.Model):
    __tablename__ = 'People'
    
    PeopleID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(100))
    
    # Relationships
    member = db.relationship('Member', back_populates='person', uselist=False)
    employee = db.relationship('Employee', back_populates='person', uselist=False)
    volunteer = db.relationship('Volunteer', back_populates='person', uselist=False)
    signups = db.relationship('SignUp', back_populates='person')
    requests = db.relationship('Request', back_populates='person')

class Member(db.Model):
    __tablename__ = 'Member'
    
    MemberID = db.Column(db.Integer, primary_key=True)
    PeopleID = db.Column(db.Integer, db.ForeignKey('People.PeopleID'), unique=True)
    JoinDate = db.Column(db.Date, nullable=False)
    MembershipStatus = db.Column(db.String(20), nullable=False)
    
    # Relationships
    person = db.relationship('People', back_populates='member')
    transactions = db.relationship('BorrowingTransaction', back_populates='member')

class Employee(db.Model):
    __tablename__ = 'Employee'
    
    EmployeeID = db.Column(db.Integer, primary_key=True)
    PeopleID = db.Column(db.Integer, db.ForeignKey('People.PeopleID'), unique=True)
    Position = db.Column(db.String(100), nullable=False)
    WagePerHour = db.Column(db.Float, nullable=False)
    
    # Relationships
    person = db.relationship('People', back_populates='employee')
    organized_events = db.relationship('Organizes', back_populates='employee')

class Event(db.Model):
    __tablename__ = 'Event'
    
    EventID = db.Column(db.Integer, primary_key=True)
    EventName = db.Column(db.String(100), nullable=False)
    Type = db.Column(db.String(50))
    EventDate = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    locations = db.relationship('IsHeldAt', back_populates='event')
    audiences = db.relationship('Recommended', back_populates='event')
    organizers = db.relationship('Organizes', back_populates='event')
    signups = db.relationship('SignUp', back_populates='event')

class AudienceType(db.Model):
    __tablename__ = 'AudienceType'
    
    AudienceTypeID = db.Column(db.Integer, primary_key=True)
    AudienceName = db.Column(db.String(50), nullable=False)
    MinAge = db.Column(db.Integer)
    MaxAge = db.Column(db.Integer)
    
    # Relationships
    events = db.relationship('Recommended', back_populates='audience')

class EventLocation(db.Model):
    __tablename__ = 'EventLocation'
    
    LocationID = db.Column(db.Integer, primary_key=True)
    RoomName = db.Column(db.String(50), nullable=False)
    Capacity = db.Column(db.Integer)
    
    # Relationships
    events = db.relationship('IsHeldAt', back_populates='location')

class Item(db.Model):
    __tablename__ = 'Item'
    
    ItemID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    PublicationYear = db.Column(db.Integer)
    Author = db.Column(db.String(100))
    Type = db.Column(db.String(50), nullable=False)  # Book, Magazine, Journal, CD, Record, etc.
    
    # Relationships
    digital_item = db.relationship('DigitalItem', back_populates='item', uselist=False)
    physical_item = db.relationship('PhysicalItem', back_populates='item', uselist=False)
    transactions = db.relationship('BorrowingTransaction', back_populates='item')

    @classmethod
    def donate_item(cls, title, author, publication_year, item_type, url=None):
        """
        Donate a new item to the library.
        
        Args:
            title (str): Title of the item
            author (str): Author of the item
            publication_year (int): Year of publication
            item_type (str): Type of item (Book, Magazine, Scientific Journal, CD, Record)
            url (str, optional): URL for digital items
            
        Returns:
            Item: The newly created item
        """
        # Create the base item
        new_item = cls(
            Title=title,
            Author=author,
            PublicationYear=publication_year,
            Type=item_type,
            Status='Available'  # New items start as Available
        )
        
        db.session.add(new_item)
        db.session.flush()  # Get the ItemID
        
        # Create the specific item type (Physical or Digital)
        if url:  # If URL is provided, it's a digital item
            digital_item = DigitalItem(
                ItemID=new_item.ItemID,
                URL=url
            )
            db.session.add(digital_item)
        else:  # If no URL, it's a physical item
            physical_item = PhysicalItem(
                ItemID=new_item.ItemID,
                ShelfNumber="TBD"  # Temporary value until staff assigns it
            )
            db.session.add(physical_item)
        
        db.session.commit()
        return new_item

class DigitalItem(db.Model):
    __tablename__ = 'DigitalItem'
    
    ItemID = db.Column(db.Integer, db.ForeignKey('Item.ItemID'), primary_key=True)
    URL = db.Column(db.String(200), nullable=False)
    
    # Relationships
    item = db.relationship('Item', back_populates='digital_item')

class PhysicalItem(db.Model):
    __tablename__ = 'PhysicalItem'
    
    ItemID = db.Column(db.Integer, db.ForeignKey('Item.ItemID'), primary_key=True)
    ShelfNumber = db.Column(db.String(20), nullable=False)
    
    # Relationships
    item = db.relationship('Item', back_populates='physical_item')

class ProposedItem(db.Model):
    __tablename__ = 'ProposedItem'
    
    ProposalID = db.Column(db.Integer, primary_key=True)
    ProposalDate = db.Column(db.Date, nullable=False)
    IntendedType = db.Column(db.String(20), nullable=False)
    Title = db.Column(db.String(100))
    Author = db.Column(db.String(100))

class BorrowingTransaction(db.Model):
    __tablename__ = 'BorrowingTransaction'
    
    TransactionID = db.Column(db.Integer, primary_key=True)
    MemberID = db.Column(db.Integer, db.ForeignKey('Member.MemberID'), nullable=False)
    ItemID = db.Column(db.Integer, db.ForeignKey('Item.ItemID'), nullable=False)
    CheckoutDate = db.Column(db.DateTime, nullable=False)
    DueDate = db.Column(db.DateTime, nullable=False)
    ReturnDate = db.Column(db.DateTime)
    
    # Relationships
    member = db.relationship('Member', back_populates='transactions')
    item = db.relationship('Item', back_populates='transactions')
    fine = db.relationship('Fine', back_populates='transaction', uselist=False)

class Fine(db.Model):
    __tablename__ = 'Fine'
    
    FineID = db.Column(db.Integer, primary_key=True)
    TransactionID = db.Column(db.Integer, db.ForeignKey('BorrowingTransaction.TransactionID'), nullable=False)
    Amount = db.Column(db.Float, nullable=False)
    DateReturned = db.Column(db.Date)
    PaidDate = db.Column(db.Date)
    PaidStatus = db.Column(db.Boolean, default=False)
    
    # Relationships
    transaction = db.relationship('BorrowingTransaction', back_populates='fine')

class Request(db.Model):
    __tablename__ = 'Request'
    
    RequestID = db.Column(db.Integer, primary_key=True)
    PeopleID = db.Column(db.Integer, db.ForeignKey('People.PeopleID'), nullable=False)
    Question = db.Column(db.Text, nullable=False)
    Answer = db.Column(db.Text)
    
    # Relationships
    person = db.relationship('People', back_populates='requests')

class IsHeldAt(db.Model):
    __tablename__ = 'IsHeldAt'
    
    EventID = db.Column(db.Integer, db.ForeignKey('Event.EventID'), primary_key=True)
    LocationID = db.Column(db.Integer, db.ForeignKey('EventLocation.LocationID'), primary_key=True)
    
    # Relationships
    event = db.relationship('Event', back_populates='locations')
    location = db.relationship('EventLocation', back_populates='events')

class Recommended(db.Model):
    __tablename__ = 'Recommended'
    
    EventID = db.Column(db.Integer, db.ForeignKey('Event.EventID'), primary_key=True)
    AudienceTypeID = db.Column(db.Integer, db.ForeignKey('AudienceType.AudienceTypeID'), primary_key=True)
    
    # Relationships
    event = db.relationship('Event', back_populates='audiences')
    audience = db.relationship('AudienceType', back_populates='events')

class Organizes(db.Model):
    __tablename__ = 'Organizes'
    
    EmployeeID = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeID'), primary_key=True)
    EventID = db.Column(db.Integer, db.ForeignKey('Event.EventID'), primary_key=True)
    
    # Relationships
    employee = db.relationship('Employee', back_populates='organized_events')
    event = db.relationship('Event', back_populates='organizers')

class SignUp(db.Model):
    __tablename__ = 'SignUp'
    
    RegistrationID = db.Column(db.Integer, primary_key=True)
    EventID = db.Column(db.Integer, db.ForeignKey('Event.EventID'), nullable=False)
    PeopleID = db.Column(db.Integer, db.ForeignKey('People.PeopleID'), nullable=False)
    Attended = db.Column(db.Boolean, default=False)
    
    # Relationships
    event = db.relationship('Event', back_populates='signups')
    person = db.relationship('People', back_populates='signups')

class IsDue(db.Model):
    __tablename__ = 'IsDue'
    
    FineID = db.Column(db.Integer, db.ForeignKey('Fine.FineID'), primary_key=True)
    TransactionID = db.Column(db.Integer, db.ForeignKey('BorrowingTransaction.TransactionID'), primary_key=True)

class Volunteer(db.Model):
    __tablename__ = 'Volunteer'
    
    VolunteerID = db.Column(db.Integer, primary_key=True)
    PeopleID = db.Column(db.Integer, db.ForeignKey('People.PeopleID'), unique=True)
    JoinDate = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(20), nullable=False)  # Active, Inactive
    Role = db.Column(db.String(100), nullable=False)  # e.g., "Book Shelver", "Event Helper"
    
    # Relationships
    person = db.relationship('People', back_populates='volunteer')