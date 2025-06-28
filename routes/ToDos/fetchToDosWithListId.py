from flask import request, jsonify
from models.ToDos import ToDos
import jwt
import os
from dotenv import load_dotenv

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

def fetchToDosWithListId():
    # 🔐 Auth check
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    user_id, error = verify_token(token)
    if error:
        return jsonify(error), 401

    # ✅ Get listId from query params
    list_id = request.args.get("listId")
    if not list_id:
        return jsonify({"error": "Missing listId in query params"}), 400

    # 📄 Pagination
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Page and limit must be integers"}), 400

    offset = (page - 1) * limit

    # 🔍 Filter todos by user and list
    total = ToDos.query.filter_by(user_id=user_id, list_id=list_id, delete=False).count()
    todos = ToDos.query.filter_by(user_id=user_id, list_id=list_id, delete=False)\
                       .order_by(ToDos.create_time.desc())\
                       .offset(offset)\
                       .limit(limit)\
                       .all()

    # 🔄 Serialize
    todos_list = [todo.serialize() for todo in todos]

    return jsonify({
        "todos": todos_list,
        "page": page,
        "limit": limit,
        "total": total
    }), 200
