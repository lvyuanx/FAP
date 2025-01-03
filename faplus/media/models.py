#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: models.py
Author: lvyuanxiang
Date: 2024/11/13 15:25:10
Description: 权限模块模型
"""
from tortoise import fields
from tortoise.models import Model

from faplus.utils import time_util

class FileRecord(Model):
    
    id = fields.IntField(pk=True, description="自增主键，用于唯一标识每个文件记录")
    original_name = fields.CharField(max_length=255, description="文件的真实名称，用户上传的文件名")
    file_hash = fields.CharField(max_length=64, description="文件的哈希值（SHA256），用于唯一标识文件")
    file_path = fields.CharField(max_length=512, description="文件存储在服务器上的路径")
    file_type = fields.CharField(max_length=50, description="文件类型（如：image/jpeg，application/pdf 等），根据 MIME 类型")
    source = fields.CharField(max_length=255, null=True, description="文件的来源（如上传者、系统等），可以为空")
    created_at = fields.IntField(default=time_util.now_timestamp(), description="文件的保存时间")


    class Meta:
        table = "file_record"
        description = "文件记录表"
        
        indexes = [
            ("file_hash", "file_path"),  # 创建联合索引，包含 file_hash 和 file_path 字段
        ]

    def __str__(self):
        return f"FileRecord(id={self.id}, original_name={self.original_name}, file_hash={self.file_hash})"

