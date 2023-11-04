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
    
    @app.route('/', methods=['POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash("No selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print("File uploaded")
                document_ids = []
                document = Document(content = file.read().decode('utf-8'))
                print("document:", document)
                # try:
                #     db.session.add(document)
                #     db.session.commit()
                #     document_ids.append(document.document_id)
                # except Exception as e:
                #     return jsonify({"error": str(e)})
                return redirect(url_for('upload_file', name = filename))
        return 
    ## ---------------------------------------------------------------------------- ##
    ## Logic for submitting the documents
    ## ---------------------------------------------------------------------------- ##

    @app.route('/submit-document', methods=["POST"])
    def submit_document():
        uploaded_files = request.files.getlist('fileInput')
        document_ids = []
        
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                print("Recieved file:", file.filename)
                document = Document(content = file.read().decode('utf-8'))
                db.session.add(document)
                db.session.commit()
                document_ids.append(document.document_id)

        if document_ids:
            response = {
                'document_ids': document_ids,
                'message': 'Documents uploaded successfully'
            }
            return jsonify(response)
        else:
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
            if "documents" in data:
                documents = data["documents"]

                # Concatenate all documents into a single text
                combined_text = "\n".join(documents)

                # Generate a summary based on the combined text
                summary = generate_summary(combined_text)

                ## TODO Instaed of returning the summary, save it in Summary table in DB
                return jsonify({"summary": summary})
            else:
                return jsonify({"error": "No documents provided"}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return app, db
