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

from core.faplus.schema import ResponseSchema
from core.faplus.utils.api_util import Response
from core.faplus.utils.config_util import StatusCodeEnum

logger = logging.getLogger("sys")


class BaseView:
    router = APIRouter()
    methods = ["POST"]
    path = ""
    name = ""
    code = ""
    response_model = ResponseSchema

    @staticmethod
    async def api():
        """抽象方法，需在子类中实现"""
        raise NotImplementedError("Subclasses should implement this method")


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
