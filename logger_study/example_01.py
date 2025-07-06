import logging
from logging.config import dictConfig
import pythonjsonlogger
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,       # 이미 생성된 로거 유지
    "formatters": {
        "json": {                            # 포맷터 이름
            "()": pythonjsonlogger.json.JsonFormatter,  # 호출 가능 객체
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",    # 표준 출력
        }
    },
    "root": {                                # 최상위(root) 로거
        "level": "INFO",
        "handlers": ["console"],
    },
}
logging.config.dictConfig(LOGGING_CONFIG) # 얘는 루트로거에 들어가는 config 이고
#dictConfig(LOGGING_CONFIG)

root_logger = logging.getLogger()
print("root_logger_handlers",root_logger.handlers)
print("root_logger_propagate",root_logger.propagate)
print("root_logger_level",root_logger.level)
print("root_logger_formatter",root_logger.handlers[0].formatter)
print(root_logger.manager.loggerDict)


ex_logger = logging.getLogger(name="example") # 얘는 루트로거로 부터 상속받는데 왜 핸들러가 없지? -> handler 상속 x
ex_logger.setLevel(logging.DEBUG)
print(ex_logger.handlers)

print(ex_logger.level)
print(ex_logger.propagate)

print(ex_logger.info(msg="hello"))


def effective_handlers(logger):
    seen = set()
    current = logger
    while current:
        for h in current.handlers:
            if h not in seen:
                yield h
                seen.add(h)
        if not current.propagate:
            break
        current = current.parent
print(list(effective_handlers(ex_logger)))