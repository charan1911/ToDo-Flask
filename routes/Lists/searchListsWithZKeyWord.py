from flask import request, jsonify
from models.Lists import Lists
import jwt
import os
from dotenv import load_dotenv
from Common.db import db

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

def searchListsWithZKeyWord():
    user_id, error, status = verify_token()
    if error:
        return jsonify(error), status

    keyword = request.args.get("z")
    if not keyword:
        return jsonify({"error": "Search keyword (z) is required"}), 400

    # Case-insensitive search using ilike
    lists = Lists.query.filter(
        Lists.user_id == user_id,
        Lists.name.ilike(f"%{keyword}%")
    ).all()

    response = [{"listId": lst.ListId, "listName": lst.name} for lst in lists]

    return jsonify(response), 200
