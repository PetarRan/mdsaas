from flask_sqlalchemy import SQLAlchemy
from app import db

class Document(db.Model):
    __tablename__ = 'document'
    document_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    upload_date = db.Column(db.Timestamp)

class Summary(db.Model):
    __tablename__ = 'summary'
    summary_id = db.Column(db.Integer, primary_key=True)
    generated_summary = db.Column(db.Text)

class documentSummaryAssociation(db.Model):
    __tablename__ = 'document_summary_association'
    association_Id = db.Column(db.Integer, primary_key=True)
    summary_id = db.Column(db.Integer, db.ForeignKey('summary.summary_id'))
    document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))

def _saveDocuments(documents):
    document_ids = []
    for contentLoc in documents:
        document = Document(content=contentLoc)
        
        ## Save the document in DB
        db.session.add(document)
        db.session.commit()
        document_ids.append(document.document_id)
    
    return document_ids

def _getAllSummaries(document_ids):
    summaries = []
    for doc_id in document_ids:
        document = Document.query.get(doc_id)
        if document:
            summary = Summary.query.filter_by(document_id=doc_id).first()
            summaries.append(
                {
                    'document_ids': document_ids,
                    'summary' : summary.content if summary else 'Summary not successful.'
                }
            )
    return summaries
