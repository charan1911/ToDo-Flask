from flask import request, jsonify
from models.ToDos import ToDos
from models.Lists import Lists
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

def createToDosWithListId():
    # 🔐 Check Authorization Header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    user_id, error = verify_token(token)
    if error:
        return jsonify(error), 401

    # 📥 Validate Request Body
    data = request.get_json()
    task_name = data.get("taskName")
    list_id = data.get("listId")

    if not task_name or not list_id:
        return jsonify({"error": "Missing taskName or listId"}), 400

    # ✅ Optionally check if list exists for this user
    list_exists = Lists.query.filter_by(ListId=list_id, user_id=user_id).first()
    if not list_exists:
        return jsonify({"error": "List not found or unauthorized"}), 404

    # 🛠️ Create Task
    new_task = ToDos(
        name=task_name,
        list_id=list_id,
        user_id=user_id,
        create_time=datetime.utcnow()  # ✅ Match your model field
    )

    new_task.save()  # Assuming your model has a save() method or you use db.session

    return jsonify({"message": "Task created successfully"}), 201
