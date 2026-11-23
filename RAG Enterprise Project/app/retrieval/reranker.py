
from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        question: str,
        chunks: list[dict],
        top_k: int = 5
    ) -> list[dict]:

        if not chunks:
            return []

        # Create question and document pairs
        pairs = [
            (question, chunk["text"])
            for chunk in chunks
        ]

        # Predict relevance scores
        scores = self.model.predict(pairs)

        # Attach scores to chunks
        reranked_results = []

        for chunk, score in zip(chunks, scores):

            result = chunk.copy()

            result["rerank_score"] = float(score)

            reranked_results.append(result)

        # Sort by cross-encoder relevance score
        reranked_results.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k]


reranker = Reranker()
