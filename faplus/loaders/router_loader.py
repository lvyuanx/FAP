#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: router_loader.py
Author: lvyuanxiang
Date: 2024/11/07 09:12:38
Description: 加载路由
"""

from collections import defaultdict
import importlib
import logging
from types import ModuleType
import uuid

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from faplus.utils.config_util import settings, StatusCodeEnum, dft_settings
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

APPLIICATION_ROOT = getattr(settings, "APPLICATION_ROOT")  # 程序根app路径
FAP_DOCS_URL = getattr(settings, "FAP_DOCS_URL", dft_settings.FAP_DOCS_URL)
FAP_REDOC_URL = getattr(settings, "FAP_REDOC_URL", dft_settings.FAP_REDOC_URL)
FAP_DOC_IS_LOCAL_STATIC = getattr(
    settings, "FAP_DOC_IS_LOCAL_STATIC", dft_settings.FAP_DOC_IS_LOCAL_STATIC)
FAP_STATIC_URL = getattr(settings, "FAP_STATIC_URL",
                         dft_settings.FAP_STATIC_URL)
FAP_STATIC_NAME = getattr(settings, "FAP_STATIC_NAME",
                          dft_settings.FAP_STATIC_NAME)
FAP_TITLE = getattr(settings, "FAP_TITLE", dft_settings.FAP_TITLE)
FAP_DESCRIPTION = getattr(settings, "FAP_DESCRIPTION",
                          dft_settings.FAP_DESCRIPTION)
FAP_VERSION = getattr(settings, "FAP_VERSION", dft_settings.FAP_VERSION)
FAP_CONTACT = getattr(settings, "FAP_CONTACT", dft_settings.FAP_CONTACT)
FAP_LICENSE = getattr(settings, "FAP_LICENSE", dft_settings.FAP_LICENSE)
FAP_OPENAPI_URL = getattr(settings, "FAP_OPENAPI_URL",
                          dft_settings.FAP_OPENAPI_URL)
FAP_APP_DEBUG = getattr(settings, "FAP_APP_DEBUG", dft_settings.FAP_APP_DEBUG)
FAP_API_CODE_NUM = getattr(
    settings, "FAP_API_CODE_NUM", dft_settings.FAP_API_CODE_NUM)
FAP_API_EXAMPLE_ADAPTER = getattr(
    settings, "FAP_API_EXAMPLE_ADAPTER", dft_settings.FAP_API_EXAMPLE_ADAPTER)
FAP_INSERTAPPS = getattr(settings, "FAP_INSERTAPPS",
                         dft_settings.FAP_INSERTAPPS)
DEBUG = getattr(settings, "DEBUG", dft_settings.DEBUG)


logger = logging.getLogger(__package__)


def init_app() -> FastAPI:
    """初始化app"""
    fap_kwargs = {
        "docs_url": FAP_DOCS_URL if DEBUG else None,
        "redoc_url": FAP_REDOC_URL if DEBUG else None,
        "title": FAP_TITLE,
        "description": FAP_DESCRIPTION,
        "version": FAP_VERSION,
        "contact": FAP_CONTACT,
        "license_info": FAP_LICENSE,
        "openapi_url": FAP_OPENAPI_URL if DEBUG else None,
        "debug": FAP_APP_DEBUG if DEBUG else False,
    }
    app = FastAPI(**fap_kwargs)
    if FAP_DOC_IS_LOCAL_STATIC:
        app.docs_url = None
        app.redoc_url = None
        app.mount(FAP_STATIC_URL, StaticFiles(
            directory=FAP_STATIC_NAME), name="fap_static")

        @app.get(FAP_DOCS_URL, include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url="/static/swagger-ui-bundle.js",
                swagger_css_url="/static/swagger-ui.css",
            )

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()

        @app.get(FAP_REDOC_URL, include_in_schema=False)
        async def redoc_html():
            return get_redoc_html(
                openapi_url=app.openapi_url,
                title=app.title + " - ReDoc",
                redoc_js_url="/static/redoc.standalone.js",
            )

    return app


def generate_examples(msgs: list[tuple], append_codes: list[StatusCodeEnum]):
    """生成结果示例

    :param msgs: (状态码，描述)
    :return: 返回示例
    """
    if FAP_API_EXAMPLE_ADAPTER:
        adapter = importlib.import_module(FAP_API_EXAMPLE_ADAPTER)
    else:
        from ..adapters import example_adapater as adapter
    example = []
    success_example = adapter.success()
    example.append(success_example)
    for code, msg in msgs:
        error_example = adapter.error(code, msg)
        example.append(error_example)
    for code in append_codes:
        error_example = adapter.error(code.value, code.name)
        example.append(error_example)
    return example


def check_module(module: ModuleType):
    app_name = module.__name__.split('.views.', 1)[0]
    if app_name not in FAP_INSERTAPPS:
        raise RuntimeError(f"{app_name} app is not in FAP_INSERTAPPS")


def loader(*args, **kwargs):
    api_module = f"{APPLIICATION_ROOT}.apis"

    # 加载路由配置
    apis_module = importlib.import_module(api_module)
    api_cfg = apis_module.apis

    # 初始化app
    app = init_app()

    status_dict = defaultdict(list)
    pre_len = int(FAP_API_CODE_NUM) * 2  # 接口码长度
    for name, value in StatusCodeEnum.__members__.items():  # 遍历状态码
        code = value.value
        if isinstance(code, str):  # 状态码为字符串
            status_dict[code if len(code) < pre_len else code[:pre_len]].append(
                (code, name))
        else:
            code, desc = code
            status_dict[code[:pre_len]].append({code, desc})

    # 遍历路由组
    for gid, gurl, groups, gtag in api_cfg:
        api_group = APIRouter()
        for pre_url, api_cfgs in groups.items():

            for api_cfg in api_cfgs:
                if len(api_cfg) == 4:
                    aid, aurl, amodule_or_str, aname = api_cfg
                    tags = []
                else:
                    aid, aurl, amodule_or_str, aname, tags = api_cfg
                # 获取接口模块
                if isinstance(amodule_or_str, str):
                    api_module = importlib.import_module(amodule_or_str)
                else:
                    api_module = amodule_or_str
                check_module(api_module)
                view_endpoint = api_module.View  # 视图函数
                append_codes = view_endpoint.append_codes
                api_code = str(gid) + str(aid)
                examples = generate_examples(
                    status_dict[api_code], append_codes)
                # API 配置
                api_cfg = {
                    "path": pre_url+aurl,
                    "name": f"{aname}  {api_code}",
                    "response_model": view_endpoint.response_model,
                    "methods": view_endpoint.methods,
                    "operation_id": f"{api_code}_{api_module.__name__}_{uuid.uuid4().hex}",
                    "responses": {
                        200: {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "example": examples
                                }
                            }
                        }
                    }
                }
                # 动态添加 API 路由，直接使用子类的 `api` 方法
                api_group.add_api_route(endpoint=view_endpoint.api, **api_cfg, tags=[
                    gtag] + tags)

        app.include_router(router=api_group, prefix=gurl)

    return app
