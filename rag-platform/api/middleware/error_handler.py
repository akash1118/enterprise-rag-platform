from fastapi.responses import JSONResponse
from core.logger import logger


async def global_exception_handler(request, exc):
    logger.error(f"Error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"}
    )