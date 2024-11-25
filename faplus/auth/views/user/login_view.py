#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_view.py
Author: lvyuanxiang
Date: 2024/11/19 16:58:53
Description: 登录视图
"""
from fastapi import Body, Request

from faplus import StatusCodeEnum, Response
from faplus.view import PostView
from faplus.auth.schemas import LoginReqSchema, UserSchema, LoginResSchema
from faplus.auth.utils import user_util
from faplus.utils import token_util, crypto_util

class View(PostView):
    
    response_model = LoginResSchema
    finally_code = StatusCodeEnum.登录失败
    common_codes = [
        StatusCodeEnum.用户名或密码错误
    ]

    @staticmethod
    async def api(request: Request, data: LoginReqSchema = Body(description="登录参数")):
        """
        data: LoginReqSchema
        """
        user = await user_util.authenticate_user(data.username, data.password)
        if not user:
            return View.make_code(StatusCodeEnum.用户名或密码错误)
        
        # 创建token
        payload = {"user_id": user.id}
        token = token_util.create_token(payload)
        
        # 解密数据
        user_dict = UserSchema.from_orm(user).dict()
        user_dict = crypto_util.secure_decrypt_obj(user_dict, ["username", "email", "mobile"])

        # 去除字段
        user_dict.pop("password")
        user_dict.pop("created_at")
        user_dict.pop("updated_at")

        return {"token": token, "user": user_dict}

