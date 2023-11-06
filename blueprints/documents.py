from flask_login import current_user, login_required
from flask import Blueprint, request, jsonify
from models import db, Document, Summary
import PyPDF2

document_bp = Blueprint("documents", __name__)

# Get all documents for the current user


@document_bp.route("/get-all-documents", methods=["GET"])
@login_required
def get_all_documents():
    documents = Document.query.filter_by(user_id=current_user.user_id).all()
    user = current_user
    document_list = []

    for doc in documents:
        document_data = {
            "name": doc.title,
            "dateUploaded": doc.upload_date.strftime("%B %d, %Y"),
            "id": doc.document_id,
            "content": doc.content,
            "user": user.username,
        }
        document_list.append(document_data)

    return jsonify(document_list)


# Delete a document by document_id for the current user
@document_bp.route("/delete-document/<int:document_id>", methods=["DELETE"])
@login_required
def delete_document(document_id):
    document = Document.query.get(document_id)
    if document:
        # Check if the document belongs to the current user
        if document.user_id == current_user.user_id:
            db.session.delete(document)
            db.session.commit()
            return jsonify({"message": f"Document with ID {document_id} deleted successfully"})
        else:
            return jsonify({"error": "You don't have permission to delete this document"}), 403
    else:
        return jsonify({"error": f"Document with ID {document_id} not found"}), 404
    

# Get content of a document
@document_bp.route('/get-document-content/<int:document_id>')
@login_required
def get_document_content(document_id):
    # Fetch the document based on document_id
    document = Document.query.get(document_id)

    if document:
        # Check if the document belongs to the current user
        if document.user_id == current_user.user_id:
            return document.content  # Assuming the 'content' attribute holds the document content
        else:
            return "Unauthorized - You don't have permission to access this document", 403
    else:
        return "Document not found", 404

# Upload a document for the current user


from flask import request, jsonify
import PyPDF2

@document_bp.route("/upload-document", methods=["POST"])
@login_required
def upload_document():
    # Check if files were sent
    if "content0" in request.files:
        document_ids = []

        for i in range(len(request.files)):
            # Get the content for each file and extract text from PDF files
            file = request.files.get(f"content{i}")
            title = request.form.get(f"title{i}", "Untitled")  # Default title if not provided

            if file.filename.lower().endswith(".pdf"):
                # This is a PDF file, extract text using PyPDF2
                pdf_text = extract_text_from_pdf(file)
                content = pdf_text
            else:
                # For non-PDF files, simply read the content
                content = file.read().decode("utf-8")

            new_document = Document(title=title, content=content, user_id=current_user.user_id)
            db.session.add(new_document)
            db.session.commit()
            document_ids.append(new_document.document_id)

        if document_ids:
            return jsonify({"document_ids": document_ids, "message": "Documents uploaded successfully"})
        else:
            return jsonify({"error": "No valid documents uploaded"}), 400
    else:
        return jsonify({"error": "No content provided"}), 400

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    except PyPDF2.utils.PdfrReadError:
        # Handle invalid or corrupted PDF files
        pdf_text = "Invalid or corrupted PDF file"
    return pdf_text



# SUMMARIES


# Get all summaries for the current user
@document_bp.route("/get-all-summaries", methods=["GET"])
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
@document_bp.route('/get-summary-content/<int:summary_id>')
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


@document_bp.route("/delete-summary/<int:summary_id>", methods=["DELETE"])
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
