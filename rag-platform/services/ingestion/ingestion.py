import chromadb
from sentence_transformers import SentenceTransformer
import uuid

from core.config import CHROMA_DB_PATH, COLLECTION_NAME

# Init
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text, chunk_size=300):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def ingest_document(text: str):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    return {"message": "Document ingested", "chunks": len(chunks)}