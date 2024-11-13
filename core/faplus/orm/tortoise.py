#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: mysql.py
Author: lvyuanxiang
Date: 2024/11/13 10:18:18
Description: 使用mysql数据库
"""
from .. import settings

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
INSERTAPPS = getattr(settings, "INSERTAPPS", [])
IS_DEBUG  = getattr(settings, "DEBUG", True)


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
            "models": ["aerich.models"] + [f"{app}.models" for app in INSERTAPPS],
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 建议不要开启，不然存储日期时会有很多坑，时区转换在项目中手动处理更稳妥。
    "timezone": TIMEZONE
}