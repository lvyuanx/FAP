#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: user_util.py
Author: lvyuanxiang
Date: 2024/11/21 09:03:50
Description: 用户工具类
"""

import logging
import re

from faplus import FAPStatusCodeException, StatusCodeEnum
from faplus.auth.models import User
from faplus.utils import crypto_util


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


logger = logging.getLogger(__package__)


async def authenticate_user(username: str, password: str, **kwargs) -> User:
    db_password = crypto_util.enc_pwd(password)
    db_username = crypto_util.secure_encrypt(username)
    user = await User.filter(username=db_username, password=db_password, is_active=True).first()
    return user


async def create_user(username: str, password: str, is_superuser: bool, **kwargs) -> User:
    """创建用户

    :param username: 用户名
    :param password: 密码
    :param is_superuser: 是否是超级用户
    :return: 用户实例
    """
    db_password = crypto_util.enc_pwd(password)
    db_username = crypto_util.secure_encrypt(username)
    
    # 验证密码强度
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
        raise ValueError("密码必须至少包含8个字符，包括字母和数字")
    
    create_kwg = {
        "username": db_username,
        "password": db_password,
        "is_superuser": is_superuser,
    }
    email = kwargs.get("email")
    if email:
        create_kwg["email"] = crypto_util.secure_encrypt(email)
    mobile = kwargs.get("mobile")
    if mobile:
        create_kwg["mobile"] = crypto_util.secure_encrypt(mobile)
    try:
        user = await User.create(**create_kwg)
    except Exception:
        logger.error(f"create data : {create_kwg}", exc_info=True)
        raise FAPStatusCodeException(StatusCodeEnum.用户创建失败)
    return user
