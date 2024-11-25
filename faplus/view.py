#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: post.py
Author: lvyuanxiang
Date: 2024/11/06 10:23:00
Description: fastapi post 视图基类
"""
import logging
import functools

from faplus import FAPStatusCodeException, settings, dft_settings
from faplus.schema import ResponseSchema
from faplus.utils.api_util import Response
from faplus.utils.config_util import StatusCodeEnum

FAP_TOKEN_TAG = getattr(settings, "FAP_TOKEN_TAG", dft_settings.FAP_TOKEN_TAG)

logger = logging.getLogger("sys")

class BaseView:
    methods = ["POST"]
    response_model = ResponseSchema
    finally_code = None # 最终异常码
    append_codes = []
    

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
                    if not isinstance(result, ResponseSchema):
                        result = Response.OK(data=result)
                    if result.code != StatusCodeEnum.请求成功:
                        logger.error(f"result: {result}")
                    else:
                        logger.debug(f"result: {result}")
                    return result
                except FAPStatusCodeException as e:
                    result = Response.FAIL(code=e.code, msg_dict=e.msg_dict, data=e.data)
                    logger.error(f"result: {result}")
                    return result
                except Exception as e:
                    logger.error("", exc_info=True)
                    if code:
                        result = Response.FAIL(code=code)
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
