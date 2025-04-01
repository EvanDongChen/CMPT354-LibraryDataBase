from flask import Blueprint, jsonify, request, make_response
from app.models import People, Member, Item, BorrowingTransaction, PhysicalItem, DigitalItem, Event, SignUp, Employee, Request, Volunteer  # Import all your models
from app.extensions import db
from datetime import datetime, timedelta
from flask_cors import cross_origin

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
        response.headers.add('Access-Control-Allow-Credentials', 'true')
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
    items_data = []
    
    for item in items:
        # Get the most recent active transaction for this item
        active_transaction = None
        if item.transactions:
            active_transaction = next(
                (t for t in item.transactions if t.ReturnDate is None),
                None
            )
        
        # Update item status based on active transaction
        current_status = 'CheckedOut' if active_transaction else 'Available'
        if item.Status != current_status:
            item.Status = current_status
            db.session.commit()
        
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
        items_data.append(item_data)
    
    return jsonify(items_data)

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
    
    for item in items:
        # Get the most recent active transaction for this item
        active_transaction = None
        if item.transactions:
            active_transaction = next(
                (t for t in item.transactions if t.ReturnDate is None),
                None
            )

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

@api_bp.route('/api/register', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def register():
    print("\n=== Registration Request Debug ===")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {dict(request.headers)}")
    print(f"Request Data: {request.get_json()}")
    
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json
    print(f"Processing registration data: {data}")
    
    required_fields = ['first_name', 'last_name', 'phone', 'email']
    
    # Check if all required fields are present
    if not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        print(f"Missing required fields: {missing_fields}")
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Check if person already exists with this phone number
    existing_person = People.query.filter_by(Phone=data['phone']).first()
    if existing_person:
        print(f"Found existing person with phone {data['phone']}")
        # If person exists, check if they're already a member
        if existing_person.member:
            print("Person is already a member")
            return jsonify({'error': 'Already registered as a member'}), 400
        
        print("Creating member record for existing person")
        # If person exists but not a member, create member record
        new_member = Member(
            PeopleID=existing_person.PeopleID,
            JoinDate=datetime.now().date(),
            MembershipStatus='Active'
        )
        db.session.add(new_member)
        try:
            db.session.commit()
            print(f"Successfully created member record with ID: {new_member.MemberID}")
            return jsonify({
                'message': 'Member registration successful',
                'member_id': new_member.MemberID,
                'people_id': existing_person.PeopleID
            }), 201
        except Exception as e:
            print(f"Error creating member record: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    print("Creating new person record")
    # Create new person
    new_person = People(
        FirstName=data['first_name'],
        LastName=data['last_name'],
        Phone=data['phone'],
        Email=data['email']
    )
    db.session.add(new_person)
    
    try:
        print("Flushing session to get PeopleID")
        db.session.flush()  # Get the PeopleID without committing
        print(f"Created person with ID: {new_person.PeopleID}")
        
        print("Creating member record")
        # Create member record
        new_member = Member(
            PeopleID=new_person.PeopleID,
            JoinDate=datetime.now().date(),
            MembershipStatus='Active'
        )
        db.session.add(new_member)
        db.session.commit()
        print(f"Successfully created member record with ID: {new_member.MemberID}")
        
        return jsonify({
            'message': 'Registration successful',
            'member_id': new_member.MemberID,
            'people_id': new_person.PeopleID
        }), 201
        
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/events/register', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def register_for_event():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    print(f"Event registration data: {request.json}")
    data = request.json
    
    # Handle new registrations (people who aren't in the system yet)
    if 'is_new_registration' in data and data['is_new_registration']:
        required_fields = ['event_id', 'first_name', 'last_name', 'phone', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields for new registration'}), 400
            
        # Check if person already exists with this phone number
        person = People.query.filter_by(Phone=data['phone']).first()
        if not person:
            # Create new person
            try:
                person = People(
                    FirstName=data['first_name'],
                    LastName=data['last_name'],
                    Phone=data['phone'],
                    Email=data['email']
                )
                db.session.add(person)
                db.session.flush()  # Get the PeopleID without committing
                
                # Now use this new person's ID for the event registration
                data['people_id'] = person.PeopleID
                print(f"Created new person with ID: {person.PeopleID}")
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f"Error creating new person: {str(e)}"}), 500
        else:
            # Person already exists, use their ID
            data['people_id'] = person.PeopleID
            print(f"Using existing person with ID: {person.PeopleID}")
    
    # Now proceed with the regular event registration
    if 'event_id' not in data or 'people_id' not in data:
        return jsonify({'error': 'Missing event_id or people_id'}), 400

    event_id = data['event_id']
    people_id = data['people_id']

    # Check if the event exists
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Check if already registered
    existing_signup = SignUp.query.filter_by(
        EventID=event_id,
        PeopleID=people_id
    ).first()
    
    if existing_signup:
        return jsonify({'error': 'Already registered for this event'}), 400

    # Create new signup
    signup = SignUp(
        EventID=event_id,
        PeopleID=people_id,
        Attended=False
    )
    
    db.session.add(signup)
    try:
        db.session.commit()
        return jsonify({
            'message': 'Successfully registered for event',
            'success': True,
            'people_id': people_id
        }), 201
    except Exception as e:
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

@api_bp.route('/api/volunteer/register', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def register_volunteer():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json
    print(f"Processing volunteer registration data: {data}")
    
    required_fields = ['people_id', 'role']
    
    # Check if all required fields are present
    if not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        print(f"Missing required fields: {missing_fields}")
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Check if person exists
    person = People.query.get(data['people_id'])
    if not person:
        print(f"Person not found with ID: {data['people_id']}")
        return jsonify({'error': 'Person not found'}), 404
    
    # Check if person is already an employee (volunteer)
    if person.employee:
        print(f"Person is already an employee/volunteer: {data['people_id']}")
        return jsonify({'error': 'Already registered as a volunteer'}), 400
    
    try:
        # Create employee record with volunteer position
        new_volunteer = Employee(
            PeopleID=data['people_id'],
            Position=f"Volunteer - {data['role']}",
            WagePerHour=0.0  # Volunteers don't get paid
        )
        db.session.add(new_volunteer)
        db.session.commit()
        print(f"Successfully created volunteer record with ID: {new_volunteer.EmployeeID}")
        
        return jsonify({
            'message': 'Volunteer registration successful',
            'volunteer_id': new_volunteer.EmployeeID,
            'success': True
        }), 201
        
    except Exception as e:
        print(f"Error during volunteer registration: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    try:
        volunteers = Volunteer.query.join(People).all()
        return jsonify([{
            'volunteer_id': vol.VolunteerID,
            'people_id': vol.PeopleID,
            'name': f"{vol.person.FirstName} {vol.person.LastName}",
            'role': vol.Role,
            'status': vol.Status,
            'join_date': vol.JoinDate.strftime('%Y-%m-%d')
        } for vol in volunteers])
    except Exception as e:
        print(f"Error getting volunteers: {str(e)}")
        return jsonify({'error': str(e)}), 500
