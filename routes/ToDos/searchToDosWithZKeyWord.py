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

def searchToDosWithZKeyWord():
    # 🔐 Token check
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    verify_result = verify_token(token)

    if len(verify_result) == 2:
        user_id, error = verify_result
        if error:
            return jsonify(error), 401
    else:
        _, error, status = verify_result
        return jsonify(error), status

    # ✅ Get listId and keyword
    list_id = request.args.get("listId")
    keyword = request.args.get("z", "")

    if not list_id:
        return jsonify({"error": "Missing listId"}), 400

    # 🔍 Search todos matching keyword
    todos = ToDos.query.filter(
        ToDos.user_id == user_id,
        ToDos.list_id == list_id,
        ToDos.delete == False,
        ToDos.name.ilike(f"%{keyword}%")  # case-insensitive match
    ).order_by(ToDos.create_time.desc()).all()

    results = [todo.serialize() for todo in todos]

    return jsonify({
        "search": keyword,
        "count": len(results),
        "results": results
    }), 200
