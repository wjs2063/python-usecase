# main.py
import uuid
import logging
from contextvars import ContextVar

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_logging.logging.same_uuid.log_config import request_id_ctx_var

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_ctx_var.set(request_id)
        try:
            response = await call_next(request)
        finally:
            request_id_ctx_var.reset(token)
        response.headers["X-Request-ID"] = request_id
        return response

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx_var.get(None)
        return True
from fastapi_logging.logging.same_uuid.log_config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(RequestIdMiddleware)


@app.get("/{test_id}")
async def root(test_id:str):
    logger.info(f"핸들러 진입, test_id: {test_id}")
    await some_internal(test_id)
    return {"message": "ok"}

async def some_internal(test_id:str):
    logger.info(f"내부 함수 동작, test_id: {test_id}")
