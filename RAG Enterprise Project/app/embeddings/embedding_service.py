
from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def generate_embeddings(
        self,
        texts: list[str],
        batch_size: int = 32
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return embeddings.tolist()

    def generate_single_embedding(
        self,
        text: str
    ) -> list[float]:

        return self.generate_embeddings([text])[0]


# Initialize the model once
embedding_service = EmbeddingService()
