from flask import Blueprint, request, jsonify
from ..models import Author
from .. import db
from flask_jwt_extended import jwt_required

authors_bp = Blueprint('authors', __name__)

@authors_bp.route('/', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    result = [{'id': a.id, 'name': a.name, 'bio': a.bio, 'country': a.country} for a in authors]
    return jsonify(result)

@authors_bp.route('/', methods=['POST'])
@jwt_required()
def add_author():
    data = request.get_json()
    author = Author(name=data['name'], bio=data.get('bio'), country=data.get('country'))
    db.session.add(author)
    db.session.commit()
    return jsonify({'message': 'Author added', 'id': author.id}), 201

@authors_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_author(id):
    author = Author.query.get_or_404(id)
    data = request.get_json()
    author.name = data.get('name', author.name)
    author.bio = data.get('bio', author.bio)
    author.country = data.get('country', author.country)
    db.session.commit()
    return jsonify({'message': 'Author updated'})

@authors_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'message': 'Author deleted'})

@authors_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def patch_author(id):
    author = Author.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        author.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Author patched'})
