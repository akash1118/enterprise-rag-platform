from fastapi import FastAPI
from pydantic import BaseModel

from services.ingestion import ingest_document
from services.retrieval import retrieve
from services.llm import generate_answer

app = FastAPI()


class DocumentRequest(BaseModel):
    text: str


class QueryRequest(BaseModel):
    query: str


@app.post("/ingest")
def ingest(req: DocumentRequest):
    return ingest_document(req.text)


@app.post("/query")
def query(req: QueryRequest):
    context = retrieve(req.query)
    answer = generate_answer(req.query, context)

    return {
        "query": req.query,
        "context": context,
        "answer": answer
    }