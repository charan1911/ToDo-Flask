from flask import request, jsonify
from models.Lists import Lists
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

def fetchListsWithUserId():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ")[1]
    user_id, error = verify_token(token)

    if error:
        return jsonify(error), 401

    # ✅ Query all lists where user_id matches
    lists = Lists.query.filter_by(user_id=user_id).all()

    # 🔄 Format the response
    response = [{"listName": lst.name, "listId": lst.ListId} for lst in lists]

    return jsonify(response), 200
