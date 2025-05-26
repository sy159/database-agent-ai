from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import api_router
from app.core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)
from app.core.logger import init_logger, logger

app = FastAPI(title="database-agent-ai")

init_logger()
logger.info("logger initialized")

# 先处理 HTTPException
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
# 再处理验证错误
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# 最后兜底所有 Exception
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(api_router, prefix="/api")
