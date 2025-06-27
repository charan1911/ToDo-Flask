from flask import request, jsonify
from models.Lists import Lists
import jwt
import os
import uuid
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

def createListsWithUserId():
    user_id, error, status = verify_token()
    if error:
        return jsonify(error), status

    data = request.get_json()
    list_name = data.get("name")

    if not list_name:
        return jsonify({"error": "List name is required"}), 400

    # 🔑 Generate a unique listId using UUID
    list_id = str(uuid.uuid4())

    new_list = Lists(
        ListId=list_id,
        name=list_name,
        user_id=user_id
    )

    try:
        db.session.add(new_list)
        db.session.commit()
        return jsonify({
            "message": "List created successfully",
            "listId": list_id,
            "name": list_name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
