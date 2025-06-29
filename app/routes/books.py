from flask import Blueprint, request, jsonify
from ..models import Book, Author, Genre
from .. import db
from flask_jwt_extended import jwt_required

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'genre': book.genre.name,
            'published_date': book.published_date.isoformat() if book.published_date else None
        })
    return jsonify(result)

@books_bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    author = Author.query.get(data['author_id'])
    genre = Genre.query.get(data['genre_id'])
    if not author or not genre:
        return jsonify({'message': 'Invalid author or genre ID'}), 400
    book = Book(
        title=data['title'],
        author_id=author.id,
        genre_id=genre.id,
        published_date=data.get('published_date')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added', 'id': book.id}), 201

@books_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    if 'author_id' in data:
        author = Author.query.get(data['author_id'])
        if not author:
            return jsonify({'message': 'Invalid author ID'}), 400
        book.author_id = author.id
    if 'genre_id' in data:
        genre = Genre.query.get(data['genre_id'])
        if not genre:
            return jsonify({'message': 'Invalid genre ID'}), 400
        book.genre_id = genre.id
    if 'published_date' in data:
        book.published_date = data['published_date']
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@books_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

@books_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def patch_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    if 'title' in data:
        book.title = data['title']
    db.session.commit()
    return jsonify({'message': 'Book patched'})
