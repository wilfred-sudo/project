from flask import jsonify

def response_message(message, status=200):
    return jsonify({'message': message}), status

