#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:19
Description: 登录中间件
"""
import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus import settings, Response as ApiResponse, StatusCodeEnum
from faplus.auth.encrypt import aes
from faplus.auth.models import User


logger = logging.getLogger(__package__)


GONGDAN_APIS = settings.GONGDAN_APIS
GONGDAN_TK_FLAG = settings.GONGDAN_TK_FLAG
FAP_AES_KEY = settings.FAP_AES_KEY


class GondanMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 获取url
        path = request.url.path
        if path in GONGDAN_APIS:
            # 获取header中的token
            token = request.headers.get(GONGDAN_TK_FLAG)
            try:
                payload = aes.decrypt(token, FAP_AES_KEY)
            except Exception:
                logger.error("解密失败", exc_info=True)
                payload = None
            if not payload or payload != "gongdan":
                logger.error("token验证失败")
                return Response(ApiResponse.fail(StatusCodeEnum.用户未登录, StatusCodeEnum.用户未登录.name).json(), headers={"Content-Type": "application/json"})
        
        return await call_next(request)
        
            
            
            
        
