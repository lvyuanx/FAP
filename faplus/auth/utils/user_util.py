#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: user_util.py
Author: lvyuanxiang
Date: 2024/11/21 09:03:50
Description: 用户工具类
"""

import json
import logging
import re

from faplus import FAPStatusCodeException, StatusCodeEnum
from faplus.auth.models import User
from faplus.auth.schemas import UserSchema
from faplus.auth import const
from faplus.cache import cache
from faplus.utils import crypto_util


logger = logging.getLogger(__package__)


async def get_user_info(**kwargs):
    """查询用户信息, 会自动加解密以及缓存数据"""
    if "id" in kwargs:  # 如果携带了id，就先用id去缓存中差
        encrypt_data = await cache.get(const.USER_CK.format(uid=kwargs["id"]))
        if encrypt_data:
            user_str = crypto_util.secure_decrypt(encrypt_data)  # 数据解密
            return json.loads(user_str)
    user = await User.filter(**kwargs, is_active=True, is_delete=False).first()
    if not user:
        raise FAPStatusCodeException(StatusCodeEnum.用户不存在)

    user_dict = UserSchema.from_orm(user).dict()
    encrypt_data = crypto_util.secure_encrypt(json.dumps(user_dict))
    await cache.set(const.USER_CK.format(uid=user.id), encrypt_data)

    return user_dict


async def authenticate_user(username: str, password: str, **kwargs) -> dict:
    try:
        db_password = crypto_util.enc_pwd(password)
        db_username = crypto_util.secure_encrypt(username)
        return await get_user_info(username=db_username, password=db_password)
    except FAPStatusCodeException as e:
        if e.code == StatusCodeEnum.用户不存在:
            return None, None
        else:
            raise e



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
        "nickname": kwargs.get("nickname"),
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
