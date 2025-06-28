from flask import request, jsonify
from models.ToDos import ToDos
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"], None
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return None, {"error": "Invalid token"}, 401

def editToDosWithToDoId():
    # 🔐 Auth check
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    verify_result = verify_token(token)

    # Handle valid and invalid tokens properly
    if len(verify_result) == 2:
        user_id, error = verify_result
        if error:
            return jsonify(error), 401
    else:
        _, error, status = verify_result
        return jsonify(error), status

    # 📥 Request body
    data = request.get_json()
    todo_id = data.get("todoId")
    name = data.get("name")
    status = data.get("status")

    if not todo_id:
        return jsonify({"error": "Missing todoId"}), 400

    # 🔍 Check if task exists and belongs to user
    todo = ToDos.query.filter_by(id=todo_id, user_id=user_id, delete=False).first()
    if not todo:
        return jsonify({"error": "ToDo not found or unauthorized"}), 404

    # ✅ Update values if provided
    if name is not None:
        todo.name = name
    if status is not None:
        todo.status = status

    todo.edit_time = datetime.utcnow()
    todo.save()

    return jsonify({"message": "ToDo updated successfully"}), 200
