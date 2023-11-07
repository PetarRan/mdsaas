from flask_login import current_user, login_required
from flask import Blueprint, request, jsonify
from models import db, Document, Summary
from summarizer.summarizer import (
    generate_summary,
) 
import PyPDF2

summarizer_bp = Blueprint("summarizer", __name__)

# Get all summaries for the current user
@summarizer_bp.route("/get-all-summaries", methods=["GET"])
@login_required
def get_all_summaries():
    summaries = Summary.query.filter_by(user_id=current_user.user_id).all()
    summary_list = []

    for summary in summaries:
        summary_data = {
            "summary_id": summary.summary_id,
            "generated_summary": summary.generated_summary,
            "method": summary.method,
        }
        summary_list.append(summary_data)

    return jsonify(summary_list)


# Get content of a summary
@summarizer_bp.route('/get-summary-content/<int:summary_id>')
@login_required
def get_summary_content(summary_id):
    # Fetch the document based on document_id
    summary = Summary.query.get(summary_id)

    if summary:
        # Check if the document belongs to the current user
        if summary.user_id == current_user.user_id:
            return summary.generated_summary  # Assuming the 'content' attribute holds the document content
        else:
            return "Unauthorized - You don't have permission to access this document", 403
    else:
        return "Document not found", 404


# Delete a summary by summary_id for the current user


@summarizer_bp.route("/delete-summary/<int:summary_id>", methods=["DELETE"])
@login_required
def delete_summary(summary_id):
    summary = Summary.query.get(summary_id)
    if summary:
        # Check if the summary belongs to the current user
        if summary.user_id == current_user.user_id:
            db.session.delete(summary)
            db.session.commit()
            return jsonify({"message": f"Summary with ID {summary_id} deleted successfully"})
        else:
            return jsonify({"error": "You don't have permission to delete this summary"}), 403
    else:
        return jsonify({"error": f"Summary with ID {summary_id} not found"}), 404
    

@summarizer_bp.route('/summarize', methods=['POST'])
@login_required
def summarize_documents():
    data = request.get_json()  # Assuming you send selected document IDs and summarization method in the request JSON
    document_ids = data.get('document_ids', [])
    summarization_method = data.get('summarization_method', 'nltk')

    # Fetch the selected documents from the database
    selected_documents = Document.query.filter(Document.id.in_(document_ids)).all()

    if not selected_documents:
        return jsonify({"error": "No documents selected for summarization"}), 400

    # Extract the content of selected documents
    document_texts = [document.content for document in selected_documents]

    # Generate the summary using the selected summarization method
    summary_text = generate_summary(document_texts, summarization_method)

    # Create a new summary in the database
    new_summary = Summary(
        generated_summary=summary_text,
        method=summarization_method,
        user_id=current_user.user_id,
    )
    db.session.add(new_summary)
    db.session.commit()

    return jsonify({"message": "Summary generated and saved successfully"})
