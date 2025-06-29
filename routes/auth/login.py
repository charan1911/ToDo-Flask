from models.user import User
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

def handle_login(data):
    if "phone" not in data or "password" not in data:
        return {"error": "Email and Password required"}, 400

    phone = data["phone"]
    password = data["password"]

    user = User.query.filter_by(phone=phone, deleted=False).first()

    if not user:
        return {"error": "User not Found"}, 404

    if user.password != password:
        return {"error": "Incorrect Password"},401
    
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"message": "Login Successful","user_id": user.id, "token": token}, 200

