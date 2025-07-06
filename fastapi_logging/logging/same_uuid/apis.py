from fastapi import APIRouter
from functools import wraps

misc_router = APIRouter()


# 테스트용 class

class LogDecorator:
    def __init__(self, logger):
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(msg="inprogress",
                             extra={"request": f"args:{args},kwargs:{kwargs}", "type": "before", "func": func.__name__})
            result = func(*args, **kwargs)
            self.logger.info(msg="inprogress", extra=f"args:{args},kwargs:{kwargs}")
            return result

        return wrapper


class TestLogging:
    def __init__(self, name):
        self.name = name

    def run(self):
        pass

    def process_request(self):
        return {"response": "process request succeed"}

    def process_filter(self):
        return {"response": "process filter succeed"}


@misc_router.get("/misc")
async def misc():
    return {"message": "misc"}
