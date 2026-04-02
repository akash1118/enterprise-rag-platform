from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    CHROMA_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "rag_collection"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = "../.env"


settings = Settings()