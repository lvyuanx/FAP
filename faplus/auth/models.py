#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: models.py
Author: lvyuanxiang
Date: 2024/11/13 15:25:10
Description: 权限模块模型
"""
from tortoise import fields
from tortoise.indexes import Index
from tortoise.models import Model

from faplus.utils import time_util


class User(Model):

    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=32, unique=True, description="用户名")
    password = fields.CharField(max_length=128, description="密码")
    nickname = fields.CharField(max_length=32, null=True, description="昵称")
    email = fields.CharField(max_length=128, null=True, unique=True, description="邮箱")
    avatar = fields.CharField(max_length=64, null=True, description="头像(图片的sn)")
    mobile = fields.CharField(
        max_length=32, null=True, unique=True, description="手机号码"
    )
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_delete = fields.BooleanField(default=False, description="是否删除")
    is_superuser = fields.BooleanField(default=False, description="是否是超级管理员")
    created_at = fields.IntField(
        default=time_util.now_timestamp(), description="创建时间"
    )
    delete_at = fields.IntField(null=True, description="删除时间")
    updated_at = fields.IntField(null=True, description="更新时间")

    class Meta:
        table = "auth_user"
        indexes = [
            Index(fields=["email"]),
            Index(fields=["mobile"]),
        ]
        description = "用户表"
