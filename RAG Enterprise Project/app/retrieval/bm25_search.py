
import re
from rank_bm25 import BM25Okapi

from app.vectorstore.collections import DEPARTMENTS, get_collection


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase tokens.
    Preserve technical identifiers such as API-401.
    """
    return re.findall(r"[a-zA-Z0-9]+(?:[-_./][a-zA-Z0-9]+)*", text.lower())


def bm25_search(
    question: str,
    departments: list[str],
    top_k: int = 5
) -> list[dict]:

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if not departments:
        raise ValueError("At least one department is required")

    query_tokens = tokenize(question)

    if not query_tokens:
        return []

    all_chunks = []

    # Retrieve stored text from each requested collection
    for department in departments:

        if department not in DEPARTMENTS:
            raise ValueError(f"Invalid department: {department}")

        collection = get_collection(department)

        stored_data = collection.get(
            include=["documents", "metadatas"]
        )

        documents = stored_data["documents"] or []
        metadatas = stored_data["metadatas"] or []
        ids = stored_data["ids"]

        for chunk_id, document, metadata in zip(
            ids, documents, metadatas
        ):
            all_chunks.append({
                "chunk_id": chunk_id,
                "text": document,
                "metadata": metadata
            })

    if not all_chunks:
        return []

    # Tokenize all stored chunks
    tokenized_documents = [
        tokenize(chunk["text"])
        for chunk in all_chunks
    ]

    # Build BM25 index for this search
    bm25 = BM25Okapi(tokenized_documents)

    # Calculate keyword relevance scores
    scores = bm25.get_scores(query_tokens)

    # Attach scores to chunks
    for chunk, score in zip(all_chunks, scores):
        chunk["bm25_score"] = float(score)

    # Sort by highest BM25 score
    ranked_results = sorted(
        all_chunks,
        key=lambda item: item["bm25_score"],
        reverse=True
    )

    # Return top matching chunks
    return [
        result
        for result in ranked_results[:top_k]
        if result["bm25_score"] > 0
    ]
