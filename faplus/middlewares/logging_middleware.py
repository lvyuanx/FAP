#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: logging_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:06
Description: 日志中间件
"""


from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging

from faplus import StatusCodeEnum, Response as ApiResponse

logger = logging.getLogger(__package__)

status_code_dict = {
    404: StatusCodeEnum.请求不存在
}

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 请求前的日志记录
        logger.info(f"Request: {request.method} {request.url.path}")
        try:
            res =  await call_next(request)
            status_code = res.status_code
            if status_code == 200:
                return res
            else: 
                logger.error(f"Response: {status_code}")
                if status_code in status_code_dict:
                    code = status_code_dict[status_code]
                    return Response(ApiResponse.FAIL(code).json(), headers={"Content-Type": "application/json"})
                return res
        except Exception as e:
            logger.error("An error occurred during request processing", exc_info=True)
            raise e
