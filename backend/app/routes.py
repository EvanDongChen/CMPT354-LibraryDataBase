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

@api_bp.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.serialize() for item in items])
