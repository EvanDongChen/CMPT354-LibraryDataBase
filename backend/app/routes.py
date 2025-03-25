from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from .models import People, Member, Item

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    person = People.query.filter_by(
        PeopleID=data.get('people_id'),
        Phone=data.get('phone')
    ).first()
    
    if person:
        access_token = create_access_token(identity=person.PeopleID)
        return jsonify({
            'success': True,
            'access_token': access_token,
            'user': {
                'id': person.PeopleID,
                'firstName': person.FirstName,
                'lastName': person.LastName
            }
        })
    return jsonify({'success': False}), 401

@api_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'This is a protected endpoint'})

# Add similar endpoints for all your models and operations
@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': i.ItemID,
        'title': i.Title,
        'status': i.Status,
        'author': i.Author,
        'type': i.Type
    } for i in items])