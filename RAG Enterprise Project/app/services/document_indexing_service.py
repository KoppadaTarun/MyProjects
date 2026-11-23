from sqlalchemy.orm import Session

from app.database.models import Document
from app.ingestion.pipeline import process_document
from app.embeddings.embedding_service import embedding_service
from app.vectorstore.vector_operations import (
    add_chunks,
    delete_document_chunks
)


def index_document(document_id: int, db: Session):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise ValueError("Document not found")

    try:
        # 1. Update document status
        document.status = "processing"
        db.commit()

        # 2. Extract, clean and split document
        chunks = process_document(
            file_path=document.file_path,
            document_id=document.id,
            department=document.department.name,
            uploaded_by=document.uploaded_by
        )

        if not chunks:
            raise ValueError("No text could be extracted from document")

        # 3. Generate embeddings
        texts = [chunk["text"] for chunk in chunks]

        embeddings = embedding_service.generate_embeddings(texts)

        # 4. Remove old vectors if this document is being reindexed
        delete_document_chunks(
            department=document.department.name,
            document_id=document.id
        )

        # 5. Store new chunks in ChromaDB
        add_chunks(
            department=document.department.name,
            chunks=chunks,
            embeddings=embeddings
        )

        # 6. Update document status
        document.status = "indexed"
        db.commit()

        return {
            "document_id": document.id,
            "filename": document.filename,
            "department": document.department.name,
            "total_chunks": len(chunks),
            "status": "indexed"
        }

    except Exception:
        db.rollback()

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        if document:
            document.status = "failed"
            db.commit()

        raise