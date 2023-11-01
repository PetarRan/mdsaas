from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from summarizer.summarizer import (
    generate_summary,
) 
from config.config import Config
from api.doc_api import (_getAllSummaries, _saveDocuments)
from models import db, Document

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def app_factory(config_name='test'):
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    @app.route("/")
    def homepage():
        return render_template("main/index.html")

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
