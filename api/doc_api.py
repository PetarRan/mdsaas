from models import db
from models import Document, Summary

def _saveDocuments(documents):
    document_ids = []
    for contentLoc in documents:
        document = Document(content=contentLoc)
        db.session.add(document)
        document_ids.append(document.document_id)
    try:
        db.session.commit()
        return document_ids
    except Exception as e:
        db.session.rollback()
        return []

def _getAllSummaries(document_ids):
    summaries = []
    for doc_id in document_ids:
        document = Document.query.get(doc_id)
        if document:
            summary = Summary.query.filter_by(document_id=doc_id).first()
            summaries.append(
                {
                    'document_ids': doc_id,
                    'summary' : summary.content if summary else 'Summary not successful.'
                }
            )
    return summaries
