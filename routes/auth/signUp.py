from models.user import User
from Common.db import db

def handle_signUp(data):
    if "phone" not in data or "name" not in data or "password" not in data:
        return {"error": "Name, Phone, and Password required"}, 400

    phone = data["phone"]
    name = data["name"]
    password = data["password"]

    existing_user = User.query.filter_by(phone=phone).first()
    if existing_user:
        return {"error": "User with that phone already exists"}, 409

    new_user = User(name=name, phone=phone, password=password, deleted=False)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201
