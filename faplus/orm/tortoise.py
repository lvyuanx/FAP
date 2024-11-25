#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: mysql.py
Author: lvyuanxiang
Date: 2024/11/13 10:18:18
Description: 使用mysql数据库
"""
import importlib
import inspect
import logging

from tortoise import Model

from .. import settings, dft_settings

logger = logging.getLogger("FAPlus")

USERNAME = getattr(settings, "DB_USERNAME", dft_settings.DB_USERNAME)
PASSWORD = getattr(settings, "DB_PASSWORD", dft_settings.DB_PASSWORD)
HOST = getattr(settings, "DB_HOST", dft_settings.DB_HOST)
PORT = getattr(settings, "DB_PORT", dft_settings.DB_PORT)
DATABASE = getattr(settings, "DB_DATABASE", dft_settings.DB_DATABASE)
ENGINE = getattr(settings, "DB_ENGINE", dft_settings.DB_ENGINE)
CHARSET = getattr(settings, "DB_CHARSET", dft_settings.DB_CHARSET)
TIMEZONE = getattr(settings, "DB_TIMEZONE", dft_settings.DB_TIMEZONE)
MAXSIZE = getattr(settings, "DB_MAXSIZE", dft_settings.DB_MAXSIZE)
MINSIZE = getattr(settings, "DB_MINSIZE", dft_settings.DB_MINSIZE)
GENERATE_SCHEMAS = getattr(settings, "DB_GENERATE_SCHEMAS", dft_settings.DB_GENERATE_SCHEMAS)
INSERTAPPS = getattr(settings, "FAP_INSERTAPPS", dft_settings.FAP_INSERTAPPS)
DEBUG  = getattr(settings, "DEBUG", dft_settings.DEBUG)


def has_model_subclasses(module):
    """
    检查模块中是否有 Model 的子类
    """
    model_subclasses = [
        cls for _, cls in inspect.getmembers(module, inspect.isclass)
        if issubclass(cls, Model) and cls is not Model
    ]
    return model_subclasses

def get_models():

    models = []
    for app in INSERTAPPS:
        try:
            model_str = f"{app}.models"
            module = importlib.import_module(model_str)
            if has_model_subclasses(module):
                models.append(model_str)
        except ModuleNotFoundError:
            pass
        except Exception:
            logger.error("Failed to import models from %s" % app, exc_info=True)

    return models

    

# Tortoise ORM 配置
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",  # MySQL or Mariadb
            "credentials": {
                "host": HOST,
                "port": PORT,
                "user": USERNAME,
                "password": PASSWORD,
                "database": DATABASE,
                "minsize": MINSIZE,
                "maxsize": MAXSIZE,
                "charset": CHARSET,
                "echo": True
            }
        }
    },
    "apps": {
        "models": {
            "models": ["aerich.models"] + get_models(),
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 建议不要开启，不然存储日期时会有很多坑，时区转换在项目中手动处理更稳妥。
    "timezone": TIMEZONE
}