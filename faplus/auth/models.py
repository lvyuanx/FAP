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



class User(Model):
    
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=32, unique=True, description="用户名")
    password = fields.CharField(max_length=128, description="密码")
    nickname = fields.CharField(max_length=32, null=True, description="昵称")
    email = fields.CharField(max_length=128, null=True, unique=True, description="邮箱")
    mobile = fields.CharField(max_length=32, null=True, unique=True, description="手机号码")
    is_active = fields.BooleanField(default=True, description="是否激活")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    
    class Meta:
        table = "user"
        indexes = [
            Index(fields=["email"]),
            Index(fields=["mobile"]),
        ]
        description = "用户表"