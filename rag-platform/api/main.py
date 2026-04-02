from fastapi import FastAPI
from api.routes import ingest, query
from api.middleware.logging import LoggingMiddleware
from api.middleware.error_handler import global_exception_handler

app = FastAPI(title="Enterprise RAG Platform")

# Middleware
app.add_middleware(LoggingMiddleware)

# Routes
app.include_router(ingest.router)
app.include_router(query.router)

# Error handler
app.add_exception_handler(Exception, global_exception_handler)