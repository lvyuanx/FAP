#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: file_util.py
Author: lvyuanxiang
Date: 2025/01/03 16:34:47
Description: 文件操作相关工具
"""
import os
import hashlib
import logging
from typing import Union

from fastapi import UploadFile

logger = logging.getLogger(__package__)


async def save_upload_file(file: UploadFile, save_path: str, file_name: str = None) -> tuple[str, str]:
    """保存上传的文件并生成哈希值作为文件名
    
    :param file: 上传的文件
    :param save_path: 保存地址
    :param file_name: 文件名称（可选）
    :return: 文件的hash和文件名
    """
    if not file:
        return None

    # 创建保存目录（如果不存在的话）
    os.makedirs(save_path, exist_ok=True)

    # 获取文件内容并计算哈希值
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()

    # 根据是否提供自定义文件名来生成新的文件名
    final_file_name = file_name if file_name else file.filename
    hash_name = f"{file_hash}_{final_file_name}"

    file_path = os.path.join(save_path, hash_name)

    # 如果文件已经存在，跳过保存
    if os.path.exists(file_path):
        return (file_hash, file_name)

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(file_content)

    # 重新设置文件指针到开头
    await file.seek(0)
    
    return (file_hash, file_name)


def delete_file(file_path: str):
    """删除文件
    
    :param file_path: 文件路径
    :return: 是否删除成功
    """
    if not os.path.exists(file_path):
        return
    os.remove(file_path)
 