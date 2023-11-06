from flask import Blueprint, request, redirect, session, jsonify, url_for
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
        return redirect('/dashboard')
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect('/login')

@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    # Check if the username is already taken
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username is already taken"}), 400

    # Create a new user
    new_user = User(username=username, password=password, email=email)

    # Add the new user to the database and commit the changes
    db.session.add(new_user)
    db.session.commit()

    # After successful registration, redirect to the login page
    return redirect('/login')

  
    