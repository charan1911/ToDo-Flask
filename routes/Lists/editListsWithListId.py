from flask import request, jsonify
from models.Lists import Lists
import jwt
import os
from Common.db import db
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

def verify_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, {"error": "Missing or invalid token"}, 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"], None, 200
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return None, {"error": "Invalid token"}, 401

def editListsWithListId():
    user_id, error, status = verify_token()
    if error:
        return jsonify(error), status

    data = request.get_json()
    list_id = data.get("listId")
    new_name = data.get("name")

    if not list_id or not new_name:
        return jsonify({"error": "listId and new name are required"}), 400

    # Fetch the list by listId and check if it belongs to the user
    list_obj = Lists.query.filter_by(ListId=list_id, user_id=user_id).first()

    if not list_obj:
        return jsonify({"error": "List not found or unauthorized"}), 404

    list_obj.name = new_name

    try:
        db.session.commit()
        return jsonify({"message": "List name updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
