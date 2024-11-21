from faplus.utils.config_util import StatusCodeEnum
from faplus.schema import ResponseSchema


class Response(object):
    @staticmethod
    def OK(msg: str = None, data: dict | str = None) -> ResponseSchema:
        return ResponseSchema(code=StatusCodeEnum.请求成功, msg=msg, data=data)

    @staticmethod
    def FAIL(code: StatusCodeEnum, msg_dict: dict = None, data: dict | str = None) -> ResponseSchema:
        msg = code.name
        if msg_dict and isinstance(code.value, tuple):
            code, msg  = code.value
            msg = msg.format(**msg_dict)
        return ResponseSchema(code=code, msg=msg, data=data)
