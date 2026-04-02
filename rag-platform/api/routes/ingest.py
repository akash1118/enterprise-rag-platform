from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ingestion.ingestion import ingest_file
from schemas.request_schema import DocumentRequest

router = APIRouter()


@router.post("/ingest-file")
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT supported")

    result = ingest_file(file.file, file.filename)
    return result