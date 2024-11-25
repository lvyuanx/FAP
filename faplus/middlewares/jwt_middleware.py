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

from faplus import settings, Response as ApiResponse, StatusCodeEnum, dft_settings
from faplus.utils import token_util
from faplus.auth.models import User


logger = logging.getLogger(__package__)

FAP_JWT_WHITES = getattr(settings, "FAP_JWT_WHITES", dft_settings.FAP_JWT_WHITES)
FAP_LOGIN_URL = getattr(settings, "FAP_LOGIN_URL", dft_settings.FAP_LOGIN_URL)
FAP_TOKEN_TAG = getattr(settings, "FAP_TOKEN_TAG", dft_settings.FAP_TOKEN_TAG)
FAP_DOCS_URL = getattr(settings, "FAP_DOCS_URL", dft_settings.FAP_DOCS_URL)
FAP_REDOC_URL = getattr(settings, "FAP_REDOC_URL", dft_settings.FAP_REDOC_URL)
FAP_STATIC_URL = getattr(settings, "FAP_STATIC_URL", dft_settings.FAP_STATIC_URL)
FAP_OPENAPI_URL = getattr(settings, "FAP_OPENAPI_URL", dft_settings.FAP_OPENAPI_URL)

whitelist = FAP_JWT_WHITES + [FAP_LOGIN_URL, FAP_DOCS_URL, FAP_REDOC_URL, FAP_OPENAPI_URL]

class JwtMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 获取url
        path = request.url.path
        if not path.startswith(FAP_STATIC_URL) and path not in whitelist:
            # 获取header中的token
            token = request.headers.get(FAP_TOKEN_TAG)
            payload = token_util.verify_token(token)
            if not payload:
                logger.error("token验证失败")
                return Response(ApiResponse.fail(StatusCodeEnum.用户未登录).json(), headers={"Content-Type": "application/json"})
            
            user = await User.filter(id=payload.get("user_id")).first()
            if not user:
                logger.error("TOKEN无效")
                return Response(ApiResponse.fail(StatusCodeEnum.TOKEN无效).json(), headers={"Content-Type": "application/json"})
            request.state.user = user
        
        return await call_next(request)
        
            
            
            
        
