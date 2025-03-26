from flask import Blueprint, jsonify, request, make_response
from app.models import People, Member, Item, BorrowingTransaction  # Import all your models
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
