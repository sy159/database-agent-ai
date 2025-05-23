from typing import Dict, Any


class Code(object):
    def __init__(self, code: int, msg: str):
        """
        统一错误码结构定义，用于业务响应、异常处理。

        Attributes:
            code (int): 错误码，如 0 表示成功，1xxxx 表示业务错误。
            msg (str): 错误描述信息。
        """
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "msg": self.msg,
        }

    def __str__(self) -> str:
        return f"{self.code}-{self.msg}"


# 通用状态码
OK = Code(0, "success")
HttpOK = Code(200, "Ok")
HttpBadRequest = Code(400, "Bad Request")
HttpUnauthorized = Code(401, "Unauthorized")
HttpForbidden = Code(403, "Forbidden")
HttpNotFound = Code(404, "Not Found")
HttpInternalServerError = Code(500, "Internal Server Error")

# 自定义业务错误码（1xxxx）
TooManyRequests = Code(10101, "Too Many Requests")
