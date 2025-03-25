from flask import Blueprint, jsonify, request
from app.models import People, Member, Item  # Import all your models
from app.extensions import db

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

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    person = People.query.filter_by(
        PeopleID=data.get('people_id'),
        Phone=data.get('phone')
    ).first()
    
    if person:
        return jsonify({
            'success': True,
            'firstName': person.FirstName,
            'lastName': person.LastName
        })
    return jsonify({'success': False}), 401

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
