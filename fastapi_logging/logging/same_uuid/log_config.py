import logging.config
from pythonjsonlogger import jsonlogger
from contextvars import ContextVar


request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)

# 1️⃣ 필터는 그대로 재사용
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx_var.get(None)
        return True



LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": RequestIdFilter},
    },
    "formatters": {
        "json": {
            "()": jsonlogger.JsonFormatter,
            "fmt": "%(asctime)s %(levelname)s %(name)s %(request_id)s %(message)s",
            "json_ensure_ascii": False
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["request_id"],
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}