
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.context_builder import build_context


def retrieve_context(
    question: str,
    departments: list[str],
    top_k: int = 5,
    candidate_k: int = 15,
    max_context_chars: int = 12000
) -> dict:

    # 1. Retrieve and rerank relevant chunks
    results = hybrid_search(
        question=question,
        departments=departments,
        top_k=top_k,
        candidate_k=candidate_k
    )

    # 2. Construct final context
    context = build_context(
        chunks=results,
        max_chunks=top_k,
        max_context_chars=max_context_chars
    )

    # 3. Return context and source information
    sources = [
        {
            "document_name": result["metadata"]["document_name"],
            "department": result["metadata"]["department"],
            "page_number": result["metadata"].get("page_number", -1),
            "chunk_id": result["chunk_id"]
        }
        for result in results
    ]

    return {
        "question": question,
        "context": context,
        "sources": sources,
        "retrieved_chunks": len(results)
    }
