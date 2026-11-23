from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise RAG Assistant"
    DEBUG: bool = True

    GEMINI_API_KEY: str

    GEMINI_MODEL: str = "gemini-3.8-flash"

    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    DATABASE_URL: str = "sqlite:///./data/enterprise_rag.db"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
