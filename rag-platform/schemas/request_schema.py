from pydantic import BaseModel


class DocumentRequest(BaseModel):
    text: str


class QueryRequest(BaseModel):
    query: str