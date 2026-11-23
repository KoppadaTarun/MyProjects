from app.embeddings.embedding_service import embedding_service
from app.vectorstore.collections import DEPARTMENTS
from app.vectorstore.vector_operations import search_chunks


def semantic_search(
    question: str,
    departments: list[str],
    top_k: int = 5
) -> list[dict]:

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if not departments:
        raise ValueError("At least one department is required")

    # 1. Generate question embedding
    query_embedding = embedding_service.generate_single_embedding(
        question
    )

    all_results = []

    # 2. Search each requested department
    for department in departments:

        if department not in DEPARTMENTS:
            raise ValueError(f"Invalid department: {department}")

        results = search_chunks(
            department=department,
            query_embedding=query_embedding,
            top_k=top_k
        )

        # 3. Extract results
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        for chunk_id, document, metadata, distance in zip(
            ids, documents, metadatas, distances
        ):
            all_results.append({
                "chunk_id": chunk_id,
                "text": document,
                "metadata": metadata,
                "cosine_distance": distance,
                "cosine_similarity": 1 - distance
            })

    # 4. Sort by similarity (highest first)
    all_results.sort(
        key=lambda item: item["cosine_similarity"],
        reverse=True
    )

    # 5. Return globally best results
    return all_results[:top_k]