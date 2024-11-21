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

from .. import settings

logger = logging.getLogger("FAPlus")

USERNAME = getattr(settings, "DB_USERNAME", "root")
PASSWORD = getattr(settings, "DB_PASSWORD", "123456")
HOST = getattr(settings, "DB_HOST", "localhost")
PORT = getattr(settings, "DB_PORT", 3306)
DATABASE = getattr(settings, "DB_DATABASE", None)
ENGINE = getattr(settings, "DB_ENGINE", None)
CHARSET = getattr(settings, "DB_CHARSET", "utf8mb4")
TIMEZONE = getattr(settings, "DB_TIMEZONE", "Asia/Shanghai")
MAXSIZE = getattr(settings, "DB_MAXSIZE", 20)
MINSIZE = getattr(settings, "DB_MINSIZE", 1)
GENERATE_SCHEMAS = getattr(settings, "DB_GENERATE_SCHEMAS", False)
INSERTAPPS = getattr(settings, "FAP_INSERTAPPS", [])
IS_DEBUG  = getattr(settings, "DEBUG", True)


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