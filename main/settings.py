#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: settings.py
Author: lvyuanxiang
Date: 2024/11/07 09:54:54
Description: FAP配置文件
"""


DEBUG = False
APPLICATION_ROOT = "main"

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

INSERTAPPS = [
    "mail"
]


# *************邮件配置****************
MAIL_HOST = "smtp.163.com"
MAIL_PORT = 465
MAIL_USER = "testlv@163.com"
MAIL_PASSWORD = "LDdCSNqAsMPLRRSq"



# *************站点配置****************
SITE_CONFIG = {
    "open_shengfy": {
        # "mails": ("2466057319@qq.com", "382858170@qq.com", "763642711@qq.com", "156394694@qq.com")
        "mails": ("2466057319@qq.com",)
    },
    "pis_shengfy": {
        "mails": ("2466057319@qq.com",)
    },
    "watch_inteface": {
        "mails": ("2466057319@qq.com",)
    },
}


# *************DB****************
DB_ENGINE = "tortoise.backends.mysql"
DB_DATABASE = "test_fap" 
DB_USERNAME = "root"
DB_PASSWORD = "root"