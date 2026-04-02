import chromadb
from sentence_transformers import SentenceTransformer
import uuid
from pypdf import PdfReader
from services.chunking.chunking import smart_chunk
import google.genai as genai

from core.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=settings.COLLECTION_NAME)
genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text(file, filename: str):
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")


def chunk_text(text, chunk_size=300):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def ingest_file(file, filename: str):
    text = extract_text(file, filename)

    chunks = smart_chunk(text)
    embeddings = model.encode(chunks)
    # response = genai_client.models.embed_content(
    #     model="gemini-embedding-001",
    #     contents=chunks
    # )

    ids = [str(uuid.uuid4()) for _ in chunks]

    # embeddings = [e.values for e in response.embeddings]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=[
            {"chunk_id": i, "source": filename}
            for i in range(len(chunks))
        ]
    )

    return {
        "message": "File ingested successfully",
        "filename": filename,
        "chunks": len(chunks)
    }