#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: post.py
Author: lvyuanxiang
Date: 2024/11/06 10:23:00
Description: fastapi post 视图基类
"""
from dataclasses import MISSING
import logging
import functools

from faplus import FAPStatusCodeException, settings, dft_settings
from faplus.schema import ResponseSchema
from faplus.utils.api_util import Response
from faplus.utils.config_util import StatusCodeEnum

FAP_TOKEN_TAG = getattr(settings, "FAP_TOKEN_TAG", dft_settings.FAP_TOKEN_TAG)

logger = logging.getLogger("sys")


class ErrorInfo:
    """错误信息"""

    code: str = None
    msg: str = None
    msg_dict: dict = None

    def __init__(self, code: str, msg: str = None, msg_dict: dict = None):
        self.code = code
        self.msg = msg
        self.msg_dict = msg_dict


class BaseView:
    methods = ["POST"]
    api_code = None
    response_model = ResponseSchema
    finally_code = None  # 最终异常码
    status_codes = []  # 状态码
    common_codes = []  # 通用状态码

    code_dict = {}

    @classmethod
    def make_code(cls, code: str | StatusCodeEnum, msg_dict: dict = None) -> ErrorInfo:
        if isinstance(code, str):
            code = f"{cls.api_code}{code}"
            if code not in cls.code_dict:
                raise ValueError(f"code {code} is not register")
            msg = cls.code_dict[code]
        else:
            value = code.value
            if isinstance(value, str):
                msg = code.name
                code = value
            else:
                code, msg = value
            if code not in cls.code_dict:
                raise ValueError(f"code {code} is not register")

        return ErrorInfo(code, msg, msg_dict)

    @staticmethod
    async def api():
        """抽象方法，需在子类中实现"""
        raise NotImplementedError("Subclasses should implement this method")

    @staticmethod
    def _api_wrapper(code: StatusCodeEnum | None):
        """api wrapper with parameters"""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                """wrapper"""
                try:
                    result = await func(*args, **kwargs)
                    if isinstance(result, ErrorInfo):
                        msg_dict = result.msg_dict
                        msg = result.msg
                        if msg_dict:
                            msg = msg.format(**msg_dict)
                        result = Response.fail(code=result.code, msg=msg)
                        logger.error(f"result: {result}")
                    else:
                        result = Response.ok(data=result)
                        logger.debug(f"result: {result}")
                    return result
                except FAPStatusCodeException as e:
                    result = Response.exception(
                        code=e.code, msg_dict=e.msg_dict, data=e.data)
                    logger.error(f"result: {result}")
                    return result
                except Exception as e:
                    logger.error("", exc_info=True)
                    if code:
                        result = Response.exception(code=code)
                        logger.error(f"result: {result}")
                        return result
                    else:
                        raise e
            return wrapper
        return decorator

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # 所有api开头的方法，自动使用_api_wrapper
        for name, func in cls.__dict__.items():
            if name.startswith("api"):
                wrapped_func = cls._api_wrapper(cls.finally_code)(func)
                setattr(cls, name, wrapped_func)


class PostView(BaseView):
    methods = ["POST"]


class GetView(BaseView):
    methods = ["GET"]


class PutView(BaseView):
    methods = ["PUT"]


class DeleteView(BaseView):
    methods = ["DELETE"]


class PatchView(BaseView):
    methods = ["PATCH"]
