from flask import Blueprint, request, redirect, session, jsonify
from models import db, User
from flask_login import login_user

auth_bp = Blueprint("authentication", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username = username, password=password).first()

    if user:
        login_user(user)
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"})

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username is already taken"}), 400
    
    new_user = User(username=username, password=password, email=email)
    from tests.test_database import test_user_insertion
    test_user_insertion(new_user)
    