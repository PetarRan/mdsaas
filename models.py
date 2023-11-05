from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    registration_date = db.Column(db.Date)
    def get_id(self):
        return str(self.user_id)

class Document(db.Model):
    __tablename__ = 'document'
    document_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.Text, default="Untitled")
    content = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class Summary(db.Model):
    __tablename__ = 'summary'
    summary_id = db.Column(db.Integer, primary_key=True)
    generated_summary = db.Column(db.Text)

class documentSummaryAssociation(db.Model):
    __tablename__ = 'document_summary_association'
    association_Id = db.Column(db.Integer, primary_key=True)
    summary_id = db.Column(db.Integer, db.ForeignKey('summary.summary_id'))
    document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
