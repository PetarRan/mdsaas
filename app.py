import os
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from summarizer.summarizer import (
    generate_summary,
) 
from config.config import Config
from api.doc_api import (_getAllSummaries, _saveDocuments)
from models import db, Document
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf'}
UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def app_factory(config_name='test'):
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/")
    def homepage():
        return render_template("main/index.html")
    
    @app.route("/login")
    def loginPage():
        return render_template("auth/login.html")
    
    @app.route("/register")
    def registerPage():
        return render_template("auth/register.html")
    
    @app.route("/dashboard")
    def dashboard():
        return render_template("main/dashboard.html")


    @app.route('/submit-document', methods=["POST"])
    def submit_document():
        if 'files[]' not in request.files:
                return jsonify({"error": "No files uploaded"}), 400
        uploaded_files = request.files.getlist('files[]')
        document_ids = []

        for file in uploaded_files:
            if file and allowed_file(file.filename):
                document = Document(content=file.read().decode('utf-8'))
                document.document_id = "10204"
                db.session.add(document)
                db.session.commit()
                document_ids.append(document.document_id)

        if document_ids:
            return jsonify({"document_ids": document_ids, "message": "Documents uploaded successfully"})

        return jsonify({"error": "No valid documents uploaded"}), 400

    
    ## ---------------------------------------------------------------------------- ##
    ## Logic for retrieveing the summary
    ## ---------------------------------------------------------------------------- ##
    @app.route('/retrieve-summary', methods=['GET'])
    def retrieve_summary():
        document_ids = request.args.getlist('document_ids')
        summaries = _getAllSummaries(document_ids)

    ## ---------------------------------------------------------------------------- ##
    ## Summarization endpoint TODO: needs to take more @params (module of summarization)
    ## ---------------------------------------------------------------------------- ##
    @app.route("/summarize", methods=["POST"])
    def summarize_text():
        try:
            data = request.get_json()
            if "document_ids" in data:
                document_ids = data["document_ids"]
                documents = [Document.query.get(id).content for id in document_ids]

                # Concatenate all documents into a single text
                combined_text = "\n".join(documents)

                # Generate a summary based on the combined text
                summary = generate_summary(combined_text)

                return jsonify({"summary": summary})
            else:
                return jsonify({"error": "No document IDs provided"}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        


    @app.route("/getDocument", methods=["GET"])
    def getDocument():
        document = Document.query.get("10204")
        if document:
            return jsonify({
                'id': document.document_id,
                'content': document.content
            })
        else:
            return jsonify({'error': 'Document not found'}), 404
        
    return app, db
