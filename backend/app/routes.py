from flask import Blueprint, jsonify, request, make_response
from app.models import People, Member, Item, BorrowingTransaction, PhysicalItem, DigitalItem  # Import all your models
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
    
    person = People.query.filter_by(
        PeopleID=data.get('people_id'),
        Phone=data.get('phone')
    ).first()
    
    if person:
        # Get the member record
        member = Member.query.filter_by(PeopleID=person.PeopleID).first()
        if member:
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
            print("Person found but not a member")  # Debug log
    else:
        print("Person not found")  # Debug log
    
    response = jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    print(f"Error Response Headers: {dict(response.headers)}")
    return response

@api_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True})

@api_bp.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.serialize() for item in items])

@api_bp.route('/api/items/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '')
    if not query:
        # Return all items if search query is empty
        items = Item.query.all()
    else:
        # Search in title only, similar to find_item in library_app.py
        items = Item.query.filter(Item.Title.ilike(f'%{query}%')).all()
    
    return jsonify([item.serialize() for item in items])

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
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
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
        print(f"Item ID: {item_id}")
        
        if not item_id:
            print("Error: No item_id provided")
            return jsonify({'error': 'Item ID is required'}), 400
            
        print(f"\nChecking item status...")
        item = Item.query.get(item_id)
        if not item:
            print(f"Error: Item {item_id} not found")
            return jsonify({'error': 'Item not found'}), 404
            
        print(f"Item found: {item.Title} (Status: {item.Status})")
        
        if item.Status != 'CheckedOut':
            print(f"Error: Item {item_id} is not checked out (Status: {item.Status})")
            return jsonify({'error': 'Item is not checked out'}), 400
            
        print("\nUpdating item status...")
        item.Status = 'Available'
        
        print("\nUpdating transaction...")
        transaction = BorrowingTransaction.query.filter_by(
            ItemID=item_id,
            ReturnDate=None
        ).first()
        
        if transaction:
            transaction.ReturnDate = datetime.now()
            print("Transaction updated with return date")
        else:
            print("Warning: No active transaction found for this item")
        
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
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Error Response Headers: {dict(response.headers)}")
        return response

@api_bp.route('/api/items/donate', methods=['POST', 'OPTIONS'])
def donate_item():
    print("\n=== Donate Request Debug ===")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {dict(request.headers)}")
    print(f"Request Origin: {request.headers.get('Origin')}")
    print(f"Request Content Type: {request.headers.get('Content-Type')}")
    print(f"Request URL: {request.url}")
    print(f"Request Base URL: {request.base_url}")
    print(f"Request Path: {request.path}")
    
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
        print("\nParsing request data...")
        data = request.get_json()
        print(f"Request Data: {data}")
        
        # Validate required fields
        print("\nValidating required fields...")
        required_fields = ['title', 'author', 'publication_year', 'type']
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
            print(f"Field {field} is present: {data[field]}")
        
        # Validate item type
        print("\nValidating item type...")
        valid_item_types = ['Book', 'Magazine', 'Scientific Journal', 'CD', 'Record']
        if data['type'] not in valid_item_types:
            print(f"Invalid item type: {data['type']}")
            return jsonify({'error': f'Invalid item type. Must be one of: {", ".join(valid_item_types)}'}), 400
        
        print("\nCreating new item...")
        # Create the base item
        new_item = Item(
            Title=data['title'],
            Author=data['author'],
            PublicationYear=data['publication_year'],
            Type=data['type'],
            Status='Available'  # New items start as Available
        )
        
        print(f"New item created: {new_item.serialize()}")
        db.session.add(new_item)
        db.session.flush()  # Get the ItemID
        print(f"Item ID assigned: {new_item.ItemID}")
        
        # Create the specific item type (Physical or Digital)
        print("\nCreating specific item type...")
        if data.get('url'):  # If URL is provided, it's a digital item
            print("Creating digital item...")
            digital_item = DigitalItem(
                ItemID=new_item.ItemID,
                URL=data['url']
            )
            db.session.add(digital_item)
            print("Digital item created")
        else:  # If no URL, it's a physical item
            print("Creating physical item...")
            physical_item = PhysicalItem(
                ItemID=new_item.ItemID,
                ShelfNumber="TBD"  # Temporary value until staff assigns it
            )
            db.session.add(physical_item)
            print("Physical item created")
        
        print("\nCommitting changes to database...")
        db.session.commit()
        print("Changes committed successfully")
        
        print("\nPreparing success response...")
        response_data = {
            'message': 'Item donation submitted successfully. Library staff will process your donation.',
            'item': new_item.serialize()
        }
        print(f"Response data: {response_data}")
        
        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Response headers: {dict(response.headers)}")
        return response
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        db.session.rollback()
        error_response = jsonify({'error': str(e)}), 500
        error_response[0].headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        error_response[0].headers.add('Access-Control-Allow-Credentials', 'true')
        print(f"Error response headers: {dict(error_response[0].headers)}")
        return error_response
