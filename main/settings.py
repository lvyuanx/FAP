#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: settings.py
Author: lvyuanxiang
Date: 2024/11/07 09:54:54
Description: FAP配置文件
"""


DEBUG = True
APPLICATION_ROOT = "main"

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

OPEN_VERSION = ["", "/v1"]  # 开启的版本， "": 默认版本

FAP_MIDDLEWARE_CLASSES = [
    "faplus.middlewares.jwt_middleware.JwtMiddleware",
    "faplus.middlewares.logging_middleware.LoggingMiddleware",
]  # 中间件

FAP_STARTUP_MODULES = [
    "faplus.startups.run_info_startup",
    "faplus.cache.startups.check_cache_startup"
]  # 开机自启

FAP_SHUTDOWN_MODULES = [
    "faplus.shutdowns.close_info_shutdowns",
]  # 关机自启

FAP_JWT_WHITES = [
]  # 白名单

if DEBUG:
    FAP_JWT_WHITES += [
        "/debug/user/create",
    ]

PROJECT_APP_PACKAGES = ["mail"]  # 项目APP包

FAP_INSERTAPPS = [
    "faplus.auth"
] + PROJECT_APP_PACKAGES  # 注册的应用 框架app包+项目app包

# *************密钥****************
FAP_AES_KEY = "OUBCNUIwmA+W5UmHNm6bkkYZ47QSIRslD/gYAsIGSZg="
FAP_AES2_KEY = "abcdefghijklmnopqrstuvwx"  # 16 24 或 32 位的密钥
FAP_PUBLICK_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA30x63JVPdz14KBA/lZvq
SHhf0v2PHo1h1MqYzLmn9FaTotiIf3Knp02t9qO91heilq4xDmCYiGMukuPLt+Un
XC2Nv1c+vy+O2mu5J0NVrIsP8GccEw47gv51OA/zIZqMQTnpIDq5yx0NyGfWYQ+k
uGVkCVy8Z9EXivYyNYaT0M0T/f7VGb70aCI17MrfyCH9RsogexXRwMvQwE0TQozg
xHy3krsdIE8/HvJY8qayPA+viHmQ9Pp0kygFWbf53aBfxOLGwpW2uImI3CjthaJp
RTWGCR3XmDlPrIUXg1Tc8Ra4y8AqwCuZSovavMylUnwXnMtcUwmHomby++p2jQ8r
1QIDAQAB
-----END PUBLIC KEY-----
"""
FAP_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDfTHrclU93PXgo
ED+Vm+pIeF/S/Y8ejWHUypjMuaf0VpOi2Ih/cqenTa32o73WF6KWrjEOYJiIYy6S
48u35SdcLY2/Vz6/L47aa7knQ1Wsiw/wZxwTDjuC/nU4D/MhmoxBOekgOrnLHQ3I
Z9ZhD6S4ZWQJXLxn0ReK9jI1hpPQzRP9/tUZvvRoIjXsyt/IIf1GyiB7FdHAy9DA
TRNCjODEfLeSux0gTz8e8ljyprI8D6+IeZD0+nSTKAVZt/ndoF/E4sbClba4iYjc
KO2FomlFNYYJHdeYOU+shReDVNzxFrjLwCrAK5lKi9q8zKVSfBecy1xTCYeiZvL7
6naNDyvVAgMBAAECggEAH+xN40OoSu57g1TBVljmL0qgPmh4AcDqI9L78ca3+282
J5GHwBqq27j3/hruHJGf8aVBB6JpJBRz19WfrfBhhmTPzzNAmfIJXPIKFBIlCSgP
VQnUomfGO8W3idaD5oGy++80xCIJJj/G1Of9Zr5nCOKb4NfEap4inL/yMSNGdhLb
IDLNrS6YG323XO9eZwP97S+9Lq/YgKUrsjAZqVZoeUL90VOxtfvbK4Ra1GQfVKAk
nB6HexqTWdOzXILvYE6WkYD57FkK/Iesw5S78rILvPwpBkvg5UkuxRkCIpJ6tnzg
+zwnDE072pv44jb5R761VXYLdatr6nR2m1mVUE09EQKBgQD0Tv/YKBEw5RGpSwLT
+xIn+vQw41Z+UV8FYZhGRL9nzPomLkBELVYSgPZzMCCKWslmmU+XtN1DfHUO+TFR
SK+zjkUJOntOh1XXSjQYTeZiRAtwmnNF4uikagSWCBJvjvZF9/PsHsmRfwBztcii
u4wcUu4kvYSFr9St4ojB6x5vxQKBgQDp/BdNcHO6Sblz/SpFe+MH+69KXrq8u6/P
ODaOlh86uCzfZ+UdMrsQXkBcS7rdCopckpahG7e6OkQULJ337eK7/XfPg+jxRZZu
taXMkJ/kk4EtR62sBedGMIk6sO0oIEuX07STKBtm58f+CfMzE2xbDXESu4lZhcJW
Q2uemXD80QKBgQCqpqwLfyFS+A84I89b5xqtlpwPshzuq0QmbB+Dpe3VQdbR6Ki3
druSvUZo+4sfWX8pDZoNLCcKRts1lFcgohco4w3R/mm3Vs1dTtXIzFFK/qDHDPvM
K0252txNOGI4TrIz+ZkGrBK8cOwN50K4eSzLdBooy8DP6Rw0QfKpEeT2yQKBgAmL
F6Q37vBtK1w4ui2lVOgxcr/Ux0cFXLFV+JuuMc3iTyo5gZXESO7s+TEKga+cS3Jl
JDGkAMVetQIho7vF/xZtyyIyniChFvajAAUs7OiUv5MKNmIqx3kMZ7x2FOYrEwo5
P0c1PpDe6UBKRZoSs7uu+6qo7XwyQW/lRhFs7rfRAoGAZGg1a3T1sLPJubd6XCln
CK2+w3MNgbXAmCo0osQZE/mlfHNcywwzr4zQdpF4GuF34dYjJ5lhQqxnfNXgearb
+4yIDaJK6WCzBTRbiDw2ZCSqAXcCt0aqct+P+o0/D9iQSrr9AITZi17jDmzpy5/k
r7JtgsLMVLk+63n0NzbZL7Y=
-----END PRIVATE KEY-----
"""


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


# *************AUTH****************
# FAP_LOGIN_URL = "/login" # 自定义登录视图


# *************CACHE****************
FAP_CACHE_CONFIG = {
    "default": {
        "BACKEND": "faplus.cache.backends.redis_cache.RedisCache",
        "PREFIX": "faplus:",
        "OPTIONS": {
            "HOST": "127.0.0.1",
            "PORT": 6379,
            "DB": 0,
            "PASSWORD": "",
            "MAX_CONNECTIONS": 50,
            "ENCODING": "utf-8",
        }
    }
}
