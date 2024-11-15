#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: post.py
Author: lvyuanxiang
Date: 2024/11/06 10:23:00
Description: fastapi post 视图基类
"""
import logging
from typing import Any
import functools

from fastapi import APIRouter

from faplus.schema import ResponseSchema
from faplus.utils.api_util import Response
from faplus.utils.config_util import StatusCodeEnum

logger = logging.getLogger("sys")

class BaseView:
    methods = ["POST"]
    response_model = ResponseSchema
    finally_code = None # 最终异常码
    

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
                    return Response.OK(data=result)
                except Exception as e:
                    logger.error("", exc_info=True)
                    if code:
                        return Response.FAIL(code=code)
                    else:
                        raise e
            return wrapper
        return decorator
    
    
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls.api = cls._api_wrapper(cls.finally_code)(cls.api)

    


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
