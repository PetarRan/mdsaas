import os
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from models import db, Document, User
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from blueprints.auth import auth_bp
from blueprints.documents import document_bp
from blueprints.summarizer import summarizer_bp
from flask_login import LoginManager, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')



ALLOWED_EXTENSIONS = ('txt', 'pdf')
UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(auth_bp)
app.register_blueprint(document_bp)
app.register_blueprint(summarizer_bp)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id)) 
    if user:
        return user
    else:
        return None

def app_factory(config_name='test'):
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/")
    def homepage():
        return render_template("auth/login.html")
    
    @app.route("/login")
    def loginPage():
        return render_template("auth/login.html")
    
    @app.route("/register")
    def registerPage():
        return render_template("auth/register.html")
    
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("main/dashboard.html")
        
    return app, db
