import chromadb
from sentence_transformers import SentenceTransformer

from core.config import CHROMA_DB_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query: str, top_k: int = 3):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0]