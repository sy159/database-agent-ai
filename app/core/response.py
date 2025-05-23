from fastapi.responses import JSONResponse
from typing import Any
from app.core.error import Code, OK


def json(code: int, msg: str, data: Any = None) -> JSONResponse:
    """
    返回统一格式 JSON 响应
    """
    return JSONResponse(content={
        "code": code,
        "msg": msg,
        "data": data if data is not None else {}
    })


def success(data: Any = None) -> JSONResponse:
    """
    成功返回结构
    """
    return json(OK.code, OK.msg, data)


def fail(code: int, msg: str) -> JSONResponse:
    """
    失败响应（直接传入码和消息）
    """
    return json(code, msg)


def fail_by_code(code: Code) -> JSONResponse:
    """
    失败响应（传入 Code 实例）
    """
    return fail(code.code, code.msg)
