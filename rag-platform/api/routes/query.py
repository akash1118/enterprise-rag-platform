from fastapi import APIRouter
from services.retrieval.retrieval import retrieve
from services.llm_gateway.llm import generate_answer
from schemas.request_schema import QueryRequest
from schemas.response_schema import QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    context = retrieve(req.query)
    answer = generate_answer(req.query, context)

    return QueryResponse(
        query=req.query,
        context=context,
        answer=answer
    )