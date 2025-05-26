import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from app.core.error import (
    HttpNotFound,
    HttpBadRequest,
    HttpUnauthorized,
    HttpForbidden,
    HttpInternalServerError,
)
from app.core.response import json, fail_by_code

logger = logging.getLogger(__name__)


def http_exception_handler(request: Request, exc: Exception) -> Response:
    """
    捕获 HTTPException（404/401/403/...）。
    """
    if not isinstance(exc, StarletteHTTPException):
        # 不是 HTTPException，交给下一个 handler
        raise exc
    status = exc.status_code
    detail = exc.detail
    logger.warning(f"[HTTPException] {request.method} {request.url} → {status} {detail}")

    if status == 404:
        return fail_by_code(HttpNotFound)
    if status == 401:
        return fail_by_code(HttpUnauthorized)
    if status == 403:
        return fail_by_code(HttpForbidden)
    # 其余 HTTP 状态保留原始码和信息
    return json(code=status, msg=detail)


def validation_exception_handler(request: Request, exc: Exception) -> Response:
    """
    捕获请求验证错误（422）。
    """
    if not isinstance(exc, RequestValidationError):
        raise exc
    errors = exc.errors()
    logger.warning(f"[ValidationError] {request.method} {request.url} → {errors}")
    return json(code=HttpBadRequest.code, msg=f"参数验证失败: {errors}")


def global_exception_handler(request: Request, exc: Exception) -> Response:
    """
    兜底捕获其余所有 Exception（500）。
    """
    logger.error(f"[UnhandledException] {request.method} {request.url} → {exc}", exc_info=True)
    return fail_by_code(HttpInternalServerError)
