import math


def precision_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int = 5
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    retrieved_k = retrieved[:k]

    if not retrieved_k:
        return 0.0

    relevant_set = set(relevant)
    relevant_count = sum(
        1 for document in retrieved_k
        if document in relevant_set
    )

    return relevant_count / k


def recall_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int = 5
) -> float:
    if not relevant:
        return 0.0

    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)

    return len(retrieved_k & relevant_set) / len(relevant_set)


def mean_reciprocal_rank(
    retrieved: list[str],
    relevant: list[str]
) -> float:
    relevant_set = set(relevant)

    for rank, document in enumerate(retrieved, start=1):
        if document in relevant_set:
            return 1 / rank

    return 0.0


def ndcg_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int = 5
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    relevant_set = set(relevant)

    dcg = 0.0

    for rank, document in enumerate(retrieved[:k], start=1):
        relevance = 1 if document in relevant_set else 0
        dcg += relevance / math.log2(rank + 1)

    ideal_relevant_count = min(len(relevant_set), k)

    if ideal_relevant_count == 0:
        return 0.0

    ideal_dcg = sum(
        1 / math.log2(rank + 1)
        for rank in range(1, ideal_relevant_count + 1)
    )

    return dcg / ideal_dcg