
from app.retrieval.semantic_search import semantic_search
from app.retrieval.bm25_search import bm25_search
from app.retrieval.reranker import reranker

def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60
) -> list[dict]:

    fused_results = {}

    for results in result_lists:

        for rank, result in enumerate(results, start=1):

            chunk_id = result["chunk_id"]

            if chunk_id not in fused_results:
                fused_results[chunk_id] = {
                    **result,
                    "rrf_score": 0.0
                }

            fused_results[chunk_id]["rrf_score"] += (
                1 / (k + rank)
            )

    return sorted(
        fused_results.values(),
        key=lambda item: item["rrf_score"],
        reverse=True
    )


def hybrid_search(
    question: str,
    departments: list[str],
    top_k: int = 5,
    candidate_k: int = 10
) -> list[dict]:

    # 1. Semantic search
    semantic_results = semantic_search(
        question=question,
        departments=departments,
        top_k=candidate_k
    )

    # 2. BM25 search
    keyword_results = bm25_search(
        question=question,
        departments=departments,
        top_k=candidate_k
    )

    # 3. Combine rankings using RRF
    fused_results = reciprocal_rank_fusion(
        result_lists=[
            semantic_results,
            keyword_results
        ]
    )

    # 4. Rerank the combined candidates
    reranked_results = reranker.rerank(
        question=question,
        chunks=fused_results,
        top_k=top_k
    )

    return reranked_results
