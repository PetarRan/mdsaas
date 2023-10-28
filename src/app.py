from config.config import Config
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models.User import User
from summarizer_nltk.summarizer import (
    generate_summary,
) 

app = Flask(__name__)

def app_factory(config_name='test'):
    app.config.from_object(Config)

    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def homepage():
        return render_template("index.html")

    
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

                return jsonify({"summary": summary})
            else:
                return jsonify({"error": "No documents provided"}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return app, db, User
