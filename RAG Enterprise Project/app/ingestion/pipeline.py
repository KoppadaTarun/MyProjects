
from pathlib import Path
from uuid import uuid4

from app.ingestion.loaders import load_document
from app.ingestion.chunker import chunk_document


def process_document(
    file_path: str,
    document_id: int,
    department: str,
    uploaded_by: int
) -> list[dict]:

    # 1. Extract document text
    pages = load_document(file_path)

    # 2. Split extracted text into chunks
    chunks = chunk_document(
        pages,
        chunk_size=800,
        chunk_overlap=150
    )

    filename = Path(file_path).name

    # 3. Attach metadata to every chunk
    processed_chunks = []

    for chunk in chunks:
        processed_chunks.append({
            "chunk_id": str(uuid4()),
            "text": chunk["text"],
            "metadata": {
                "document_id": document_id,
                "document_name": filename,
                "department": department,
                "uploaded_by": uploaded_by,
                "page_number": (
                    chunk["page_number"]
                    if chunk["page_number"] is not None
                    else -1
                ),
                "chunk_index": chunk["chunk_index"]
            }
        })

    return processed_chunks
