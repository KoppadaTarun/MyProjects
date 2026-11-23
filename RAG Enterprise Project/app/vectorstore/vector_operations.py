from app.vectorstore.collections import get_collection


def add_chunks(
    department: str,
    chunks: list[dict],
    embeddings: list[list[float]]
):
    if len(chunks) != len(embeddings):
        raise ValueError("Chunks and embeddings count must match")

    if not chunks:
        return

    collection = get_collection(department)

    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=[chunk["metadata"] for chunk in chunks]
    )


def search_chunks(
    department: str,
    query_embedding: list[float],
    top_k: int = 5
):
    collection = get_collection(department)

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )


def delete_document_chunks(
    department: str,
    document_id: int
):
    collection = get_collection(department)

    collection.delete(
        where={"document_id": document_id}
    )