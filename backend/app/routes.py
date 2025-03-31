from flask import Blueprint, jsonify, request, make_response
from app.models import People, Member, Item, BorrowingTransaction, PhysicalItem, DigitalItem, Event, SignUp, Employee, Request  # Import all your models
from app.extensions import db
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

@api_bp.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([{
        'id': p.PeopleID,
        'firstName': p.FirstName,
        'lastName': p.LastName,
        'phone': p.Phone,
        'email': p.Email
    } for p in people])

@api_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    print("\n=== Login Request Debug ===")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {dict(request.headers)}")
    print(f"Request Origin: {request.headers.get('Origin')}")
    
    if request.method == 'OPTIONS':
        print("\nHandling OPTIONS request")
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"OPTIONS Response Headers: {dict(response.headers)}")
        return response

    data = request.get_json()
    print("Login attempt:", data)  # Debug log
    
    # First find the member
    member = Member.query.filter_by(MemberID=data.get('member_id')).first()
    if not member:
        print("Member not found")
        response = jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        response[0].headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response[0].headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Then verify the phone number matches
    person = People.query.filter_by(
        PeopleID=member.PeopleID,
        Phone=data.get('phone')
    ).first()
    
    if person:
        response_data = {
            'success': True,
            'firstName': person.FirstName,
            'lastName': person.LastName,
            'member_id': member.MemberID,
            'people_id': person.PeopleID
        }
        print("Login successful:", response_data)  # Debug log
        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Success Response Headers: {dict(response.headers)}")
        return response
    else:
        print("Invalid phone number for member")  # Debug log
    
    response = jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    response[0].headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response[0].headers.add('Access-Control-Allow-Credentials', 'true')
    print(f"Error Response Headers: {dict(response.headers)}")
    return response

@api_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True})

@api_bp.route('/api/items', methods=['GET'])
def get_items():
    member_id = request.args.get('member_id')
    print(f"\nFetching items for member_id: {member_id}")
    
    items = Item.query.options(db.joinedload(Item.transactions)).all()
    serialized_items = []
    
    for item in items:
        # Get the most recent active transaction for this item
        active_transaction = None
        if item.transactions:
            active_transaction = next(
                (t for t in item.transactions if t.ReturnDate is None),
                None
            )
        
        item_data = {
            'ItemID': item.ItemID,
            'Title': item.Title,
            'Status': item.Status,
            'PublicationYear': item.PublicationYear,
            'Author': item.Author,
            'Type': item.Type,
            'DueDate': active_transaction.DueDate.strftime('%Y-%m-%d') if active_transaction else None,
            'CanReturn': bool(member_id and active_transaction and str(active_transaction.MemberID) == str(member_id))
        }
        serialized_items.append(item_data)
    
    print(f"Returning {len(serialized_items)} items")
    return jsonify(serialized_items)

@api_bp.route('/api/items/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '')
    member_id = request.args.get('member_id')
    print(f"\nSearching items for query: {query}, member_id: {member_id}")
    
    if not query:
        # Return all items if search query is empty
        items = Item.query.options(db.joinedload(Item.transactions)).all()
    else:
        # Search in title only
        items = Item.query.options(db.joinedload(Item.transactions)).filter(Item.Title.ilike(f'%{query}%')).all()
    
    serialized_items = []
    for item in items:
        # Get the most recent active transaction for this item
        active_transaction = None
        if item.transactions:
            active_transaction = next(
                (t for t in item.transactions if t.ReturnDate is None),
                None
            )
        
        item_data = {
            'ItemID': item.ItemID,
            'Title': item.Title,
            'Status': item.Status,
            'PublicationYear': item.PublicationYear,
            'Author': item.Author,
            'Type': item.Type,
            'DueDate': active_transaction.DueDate.strftime('%Y-%m-%d') if active_transaction else None,
            'CanReturn': bool(member_id and active_transaction and str(active_transaction.MemberID) == str(member_id))
        }
        serialized_items.append(item_data)
    
    print(f"Returning {len(serialized_items)} items from search")
    return jsonify(serialized_items)

@api_bp.route('/api/items/borrow', methods=['POST', 'OPTIONS'])
def borrow_item():
    print("=== Borrow Request Debug ===")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {dict(request.headers)}")
    print(f"Request Origin: {request.headers.get('Origin')}")
    
    if request.method == 'OPTIONS':
        print("Handling OPTIONS request")
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"OPTIONS Response Headers: {dict(response.headers)}")
        return response

    print("Handling POST request")
    data = request.get_json()
    print(f"Request Data: {data}")
    
    member_id = data.get('member_id')
    item_id = data.get('item_id')
    print(f"Member ID: {member_id}, Item ID: {item_id}")
    
    # Check if member exists
    member = Member.query.get(member_id)
    if not member:
        print(f"Member not found: {member_id}")
        return jsonify({'success': False, 'message': 'Member does not exist'}), 404
    
    # Check item availability
    item = Item.query.get(item_id)
    if not item:
        print(f"Item not found: {item_id}")
        return jsonify({'success': False, 'message': 'Item does not exist'}), 404
    
    # Check if item is already borrowed
    active_transaction = BorrowingTransaction.query.filter_by(
        ItemID=item_id,
        ReturnDate=None
    ).first()
    
    if active_transaction:
        print(f"Item already borrowed: {item_id}")
        return jsonify({'success': False, 'message': 'Item is already borrowed'}), 400
    
    if item.Status != 'Available':
        print(f"Item not available: {item_id}, Status: {item.Status}")
        return jsonify({'success': False, 'message': 'Item is not available'}), 400
    
    try:
        print("Creating borrowing transaction")
        # Create borrowing transaction
        transaction = BorrowingTransaction(
            MemberID=member_id,
            ItemID=item_id,
            CheckoutDate=datetime.now(),
            DueDate=datetime.now() + timedelta(days=14)
        )
        
        # Update item status to 'CheckedOut'
        item.Status = 'CheckedOut'
        
        db.session.add(transaction)
        db.session.commit()
        print("Transaction created successfully")
        
        response = jsonify({
            'success': True,
            'message': 'Item borrowed successfully',
            'due_date': transaction.DueDate.strftime('%Y-%m-%d')
        })
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Success Response Headers: {dict(response.headers)}")
        return response
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.session.rollback()
        response = jsonify({'success': False, 'message': str(e)}), 500
        response[0].headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response[0].headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Error Response Headers: {dict(response.headers)}")
        return response

@api_bp.route('/api/items/return', methods=['POST', 'OPTIONS'])
def return_item_route():
    print("\n=== Return Request Debug ===")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {dict(request.headers)}")
    print(f"Request Origin: {request.headers.get('Origin')}")
    print(f"Request Data: {request.get_json()}")
    
    if request.method == 'OPTIONS':
        print("\nHandling OPTIONS request")
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"OPTIONS Response Headers: {dict(response.headers)}")
        return response

    try:
        print("\nHandling POST request")
        data = request.get_json()
        print(f"Request Data: {data}")
        item_id = data.get('item_id')
        member_id = data.get('member_id')
        print(f"Item ID: {item_id}, Member ID: {member_id}")
        
        if not item_id or not member_id:
            print("Error: No item_id or member_id provided")
            return jsonify({'error': 'Item ID and Member ID are required'}), 400
            
        print(f"\nChecking item status...")
        item = Item.query.get(item_id)
        if not item:
            print(f"Error: Item {item_id} not found")
            return jsonify({'error': 'Item not found'}), 404
            
        print(f"Item found: {item.Title} (Status: {item.Status})")
        
        if item.Status != 'CheckedOut':
            print(f"Error: Item {item_id} is not checked out (Status: {item.Status})")
            return jsonify({'error': 'Item is not checked out'}), 400
            
        # Check if this member is the one who borrowed the item
        transaction = BorrowingTransaction.query.filter_by(
            ItemID=item_id,
            MemberID=member_id,
            ReturnDate=None
        ).first()
        
        if not transaction:
            print(f"Error: Item {item_id} was not borrowed by member {member_id}")
            return jsonify({'error': 'You cannot return an item you did not borrow'}), 403
            
        print("\nUpdating item status...")
        item.Status = 'Available'
        
        print("\nUpdating transaction...")
        transaction.ReturnDate = datetime.now()
        print("Transaction updated with return date")
        
        print("\nCommitting changes...")
        db.session.commit()
        print("Changes committed successfully")
        
        response = jsonify({'message': 'Item returned successfully'})
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"\nSuccess Response Headers: {dict(response.headers)}")
        return response
    except Exception as e:
        print(f"\nError returning item: {str(e)}")
        db.session.rollback()
        response = jsonify({'error': str(e)}), 500
        response[0].headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response[0].headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Error Response Headers: {dict(response.headers)}")
        return response

@api_bp.route('/api/items/donate', methods=['POST', 'OPTIONS'])
def donate_item():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author', 'publication_year', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate item type
        valid_item_types = ['Book', 'Magazine', 'Scientific Journal', 'CD', 'Record']
        if data['type'] not in valid_item_types:
            return jsonify({'error': f'Invalid item type. Must be one of: {", ".join(valid_item_types)}'}), 400
        
        # Create the base item
        new_item = Item(
            Title=data['title'],
            Author=data['author'],
            PublicationYear=data['publication_year'],
            Type=data['type'],
            Status='Available'  # New items start as Available
        )
        
        db.session.add(new_item)
        db.session.flush()  # Get the ItemID
        
        # Create the specific item type (Physical or Digital)
        if data.get('url'):  # If URL is provided, it's a digital item
            digital_item = DigitalItem(
                ItemID=new_item.ItemID,
                URL=data['url']
            )
            db.session.add(digital_item)
        else:  # If no URL, it's a physical item
            physical_item = PhysicalItem(
                ItemID=new_item.ItemID,
                ShelfNumber="TBD"  # Temporary value until staff assigns it
            )
            db.session.add(physical_item)
        
        db.session.commit()
        
        response = jsonify({
            'message': 'Item donation submitted successfully. Library staff will process your donation.',
            'item': new_item.serialize()
        })
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    except Exception as e:
        db.session.rollback()
        error_response = jsonify({'error': str(e)}), 500
        error_response[0].headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        error_response[0].headers.add('Access-Control-Allow-Credentials', 'true')
        return error_response

@api_bp.route('/api/events', methods=['GET'])
def get_events():
    try:
        people_id = request.args.get('people_id')
        print(f"Getting events with people_id: {people_id}")
        
        events = Event.query.all()
        events_data = []
        
        for event in events:
            print(f"Processing event: {event.EventID} - {event.EventName}")
            event_data = {
                'EventID': event.EventID,
                'EventName': event.EventName,
                'Type': event.Type,
                'EventDate': event.EventDate.strftime('%Y-%m-%d %H:%M:%S'),
                'Location': event.locations[0].location.RoomName if event.locations else None,
                'Capacity': event.locations[0].location.Capacity if event.locations else None,
                'Audience': [audience.audience.AudienceName for audience in event.audiences],
                'IsRegistered': False
            }
            
            if people_id:
                # Check if user is registered for this event
                signup = SignUp.query.filter_by(
                    EventID=event.EventID,
                    PeopleID=people_id
                ).first()
                is_registered = signup is not None
                print(f"User {people_id} registration status for event {event.EventID}: {is_registered}")
                event_data['IsRegistered'] = is_registered
            
            events_data.append(event_data)
        
        print(f"Returning {len(events_data)} events")
        return jsonify(events_data)
    except Exception as e:
        print(f"Error in get_events: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/events/register', methods=['POST', 'OPTIONS'])
def register_for_event():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    try:
        data = request.get_json()
        print(f"Received registration request: {data}")
        
        if not data or 'event_id' not in data or 'people_id' not in data:
            print("Missing required fields in request")
            return jsonify({'error': 'Missing required fields'}), 400
        
        event_id = data['event_id']
        people_id = data['people_id']
        print(f"Processing registration for event {event_id} and user {people_id}")
        
        # Check if event exists
        event = Event.query.get(event_id)
        if not event:
            print(f"Event {event_id} not found")
            return jsonify({'error': 'Event not found'}), 404
        
        # Check if person exists
        person = People.query.get(people_id)
        if not person:
            print(f"Person {people_id} not found")
            return jsonify({'error': 'Person not found'}), 404
        
        # Check if already registered
        existing_signup = SignUp.query.filter_by(
            EventID=event_id,
            PeopleID=people_id
        ).first()
        
        if existing_signup:
            print(f"User {people_id} already registered for event {event_id}")
            return jsonify({'error': 'Already registered for this event'}), 400
        
        # Create new signup
        new_signup = SignUp(
            EventID=event_id,
            PeopleID=people_id,
            Attended=False
        )
        print(f"Creating new signup for event {event_id} and user {people_id}")
        
        db.session.add(new_signup)
        db.session.commit()
        print("Signup successfully created and committed")
        
        return jsonify({'message': 'Successfully registered for event'}), 200
    except Exception as e:
        print(f"Error in register_for_event: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.join(People).all()
        return jsonify([{
            'employee_id': emp.EmployeeID,
            'people_id': emp.PeopleID,
            'name': f"{emp.person.FirstName} {emp.person.LastName}",
            'position': emp.Position
        } for emp in employees])
    except Exception as e:
        print(f"Error getting employees: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/questions', methods=['GET'])
def get_questions():
    try:
        people_id = request.args.get('people_id')
        if not people_id:
            return jsonify({'error': 'People ID is required'}), 400

        questions = Request.query.filter_by(PeopleID=people_id).all()
        return jsonify([{
            'request_id': q.RequestID,
            'question': q.Question,
            'answer': q.Answer,
            'has_answer': q.Answer is not None
        } for q in questions])
    except Exception as e:
        print(f"Error getting questions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/questions', methods=['POST'])
def create_question():
    try:
        data = request.get_json()
        if not data or 'people_id' not in data or 'question' not in data:
            return jsonify({'error': 'People ID and question are required'}), 400

        new_request = Request(
            PeopleID=data['people_id'],
            Question=data['question'],
            Answer=None  # Initially no answer
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Question submitted successfully',
            'request_id': new_request.RequestID
        }), 201
    except Exception as e:
        print(f"Error creating question: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
