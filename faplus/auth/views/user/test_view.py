#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_view.py
Author: lvyuanxiang
Date: 2024/11/19 16:58:53
Description: 登录视图
"""
from fastapi import Header, Request
from faplus.view import PostView, FAP_TOKEN_TAG


class View(PostView):

    @staticmethod
    async def api(authorization: str = Header(None, description="登录token", alias=FAP_TOKEN_TAG)):
        pass
    
    
    @staticmethod
    async def api_v1():
        pass
