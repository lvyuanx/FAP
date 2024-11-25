#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: default_settings.py
Author: lvyuanxiang
Date: 2024/11/19 17:23:40
Description: FAP用到的所有默认配置
"""

DEBUG = True

# 在线文档swagger地址
FAP_DOCS_URL = "/docs"

# 在线文档redoc地址
FAP_REDOC_URL = "/redoc"

# 是否使用本地静态文件
FAP_DOC_IS_LOCAL_STATIC = False

# 静态文件地址前缀
FAP_STATIC_URL = "/static"

# 静态文件目录
FAP_STATIC_NAME = "static"

# 文档标题
FAP_TITLE = "FAP ONLINE DOCS"

# 文档说明
FAP_DESCRIPTION = ""

# 文档版本
FAP_VERSION = "0.0.1"

# 开启的版本
OPEN_VERSION = [""]

# 联系方式
FAP_CONTACT = {}

# 许可证
FAP_LICENSE = {}

# openapi接口地址
FAP_OPENAPI_URL = "/openapi.json"

# FastApi是否开启debug
FAP_APP_DEBUG = False

# api码位数
FAP_API_CODE_NUM = 2

# 文档中示例的适配器
FAP_API_EXAMPLE_ADAPTER = None

# 注册的app模块
FAP_INSERTAPPS = []

# AES加密解密(加密结果不同)
FAP_AES_KEY = None

# AES加密解密(加密结果相同)
FAP_AES2_KEY = None

# RSA公钥
FAP_PUBLICK_KEY = None

# RSA私钥
FAP_PRIVATE_KEY = None

# 密码加密
ENCRYPT_PWD = "faplus.auth.encrypt.md5"

# 铭感数据加密
COYPTO_SECURE_DATA = "faplus.auth.encrypt.aes2"

# jwt白名单
FAP_JWT_WHITES = []

# 登录地址
FAP_LOGIN_URL = "/user/login"

# token标记
FAP_TOKEN_TAG = "X-Authorization"

# 开机自启的模块
FAP_STARTUP_MODULES = []

# 关机自动触发的模块
FAP_SHUTDOWN_MODULES = []