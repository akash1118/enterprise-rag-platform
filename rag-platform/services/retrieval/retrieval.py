import chromadb
from sentence_transformers import SentenceTransformer
import google.genai as genai

from core.config import Settings

settings = Settings()
genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=settings.COLLECTION_NAME)

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query: str, top_k: int = 5):
    query_embedding = model.encode([query]).tolist()
    # result_embedding = genai_client.models.embed_content(
    #     model="gemini-embedding-001",
    #     contents=[query]
    # )
    # embeddings = [e.values for e in result_embedding.embeddings]
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0]