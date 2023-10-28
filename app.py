from flask import Flask, request, jsonify, render_template
from summarizer_nltk.summarizer import (
    generate_summary,
)  # Import the summarization function

def app_factory():
    app = Flask(__name__)

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
        
    return app;
