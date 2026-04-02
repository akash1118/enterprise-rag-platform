from pydantic import BaseModel
from typing import List


class QueryResponse(BaseModel):
    query: str
    context: List[str]
    answer: str