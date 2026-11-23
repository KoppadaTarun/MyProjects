import json
from pathlib import Path
from collections import defaultdict

from app.retrieval.semantic_search import semantic_search
from app.retrieval.bm25_search import bm25_search
from app.retrieval.hybrid_search import (
    reciprocal_rank_fusion,
    hybrid_search
)

from evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    mean_reciprocal_rank,
    ndcg_at_k
)


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "retrieval_dataset.json"

K = 2
CANDIDATE_K = 15


def load_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_unique_documents(results):
    """
    Keep only the first occurrence of each document.
    Results are already ranked, so the first occurrence
    represents the document's highest-ranked chunk.
    """
    documents = []
    seen = set()

    for result in results:
        document_name = result["metadata"]["document_name"]

        if document_name not in seen:
            documents.append(document_name)
            seen.add(document_name)

    return documents


def run_retrieval_methods(question, departments):

    semantic_results = semantic_search(
        question=question,
        departments=departments,
        top_k=CANDIDATE_K
    )

    bm25_results = bm25_search(
        question=question,
        departments=departments,
        top_k=CANDIDATE_K
    )

    hybrid_candidates = reciprocal_rank_fusion(
        [semantic_results, bm25_results]
    )

    hybrid_reranked_results = hybrid_search(
        question=question,
        departments=departments,
        top_k=CANDIDATE_K,
        candidate_k=CANDIDATE_K
    )

    return {
        "Semantic": semantic_results,
        "BM25": bm25_results,
        "Hybrid (RRF)": hybrid_candidates,
        "Hybrid + Reranking": hybrid_reranked_results
    }


def calculate_metrics(retrieved, relevant):

    return {
    "Precision@2": precision_at_k(retrieved, relevant, K),
    "Recall@2": recall_at_k(retrieved, relevant, K),
    "MRR": mean_reciprocal_rank(retrieved, relevant),
    "NDCG@2": ndcg_at_k(retrieved, relevant, K)
}


def evaluate():

    dataset = load_dataset()

    all_scores = defaultdict(list)

    for item in dataset:

        question = item["question"]
        departments = item["departments"]
        relevant_documents = item["relevant_documents"]

        print("\n" + "=" * 80)
        print("QUESTION:", question)
        print("RELEVANT DOCUMENTS:", relevant_documents)

        retrieval_results = run_retrieval_methods(
            question,
            departments
        )

        for method, results in retrieval_results.items():

            retrieved_documents = get_unique_documents(results)

            scores = calculate_metrics(
                retrieved_documents,
                relevant_documents
            )

            for metric, score in scores.items():
                all_scores[method + " | " + metric].append(score)

            print(f"\n{method}")
            print("Retrieved:", retrieved_documents)
            print("Metrics:", scores)

    print("\n\n" + "=" * 80)
    print("FINAL AVERAGE RETRIEVAL EVALUATION")
    print("=" * 80)

    for method in retrieval_results:
        print(f"\n{method}")

        for metric in [
            "Precision@2",
            "Recall@2",
            "MRR",
            "NDCG@2"
        ]:
            key = method + " | " + metric

            if all_scores[key]:
                average = sum(all_scores[key]) / len(all_scores[key])
            else:
                average = 0.0

    

            print(f"{metric}: {average:.4f}")


if __name__ == "__main__":
    evaluate()