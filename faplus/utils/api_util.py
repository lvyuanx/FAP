from faplus.utils.config_util import StatusCodeEnum
from faplus.schema import ResponseSchema


class Response(object):
    @staticmethod
    def ok(msg: str = None, data: dict | str = None) -> ResponseSchema:
        """返回正常响应

        :param msg: 消息, defaults to None
        :param data: 响应的数据, defaults to None
        :return: ResponseSchema
        """
        return ResponseSchema(code=StatusCodeEnum.请求成功, msg=msg, data=data)

    @staticmethod
    def fail(code: str, msg: str):
        return ResponseSchema(code=code, msg=msg, data=None)
