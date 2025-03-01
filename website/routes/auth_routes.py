from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import db, User
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

    new_user = User(username=data["username"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        )
        return jsonify({"token": token}), 200

    return jsonify({"message": "Invalid email or password"}), 401
