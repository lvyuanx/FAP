#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_view.py
Author: lvyuanxiang
Date: 2024/11/19 16:58:53
Description: 登录视图
"""
from fastapi import Header
from faplus.view import PostView, FAP_TOKEN_TAG


class View(PostView):

    finally_code = "00", "测试错误"
    @staticmethod
    async def api(authorization: str = Header(None, description="登录token", alias=FAP_TOKEN_TAG)):
        return View.make_code("00")
    
    
    @staticmethod
    async def api_v1():
        pass
