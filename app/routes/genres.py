from flask import Blueprint, request, jsonify
from ..models import Genre
from .. import db
from flask_jwt_extended import jwt_required

genres_bp = Blueprint('genres', __name__)

@genres_bp.route('/', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    result = [{'id': g.id, 'name': g.name, 'description': g.description} for g in genres]
    return jsonify(result)

@genres_bp.route('/', methods=['POST'])
@jwt_required()
def add_genre():
    data = request.get_json()
    genre = Genre(name=data['name'], description=data.get('description'))
    db.session.add(genre)
    db.session.commit()
    return jsonify({'message': 'Genre added', 'id': genre.id}), 201

@genres_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_genre(id):
    genre = Genre.query.get_or_404(id)
    data = request.get_json()
    genre.name = data.get('name', genre.name)
    genre.description = data.get('description', genre.description)
    db.session.commit()
    return jsonify({'message': 'Genre updated'})

@genres_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_genre(id):
    genre = Genre.query.get_or_404(id)
    db.session.delete(genre)
    db.session.commit()
    return jsonify({'message': 'Genre deleted'})

@genres_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def patch_genre(id):
    genre = Genre.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        genre.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Genre patched'})
