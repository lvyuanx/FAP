#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: media_manager.py
Author: lvyuanxiang
Date: 2025/01/03 17:11:15
Description: 媒体管理
"""
import logging
import os
from faplus import settings, dft_settings

from fastapi import UploadFile
from .utils import file_util
from .models import FileRecord

BASE_DIR = getattr(settings, 'BASE_DIR', dft_settings.BASE_DIR)
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
MEDIA_URL = getattr(settings, 'MEDIA_URL', dft_settings.MEDIA_URL)

logger = logging.getLogger(__package__)

class MediaManager:
    
    @classmethod
    async def upload(file: UploadFile, file_path: str = None, source: str = None) -> bool:
        """上传文件
        
        :param file: 上传的文件
        :param file_path: 文件路径, 会拼接上MEDIA_ROOT（可选）
        :param file_name: 文件名称（可选）
        :return: 是否成功
        """
        if file_path:
            file_path = os.path.join(MEDIA_ROOT, file_path)
        else:
            file_path = MEDIA_ROOT
        
        file_type = file.content_type

        try:
        
            # 保存文件
            file_hash, file_name = await file_util.save_upload_file(file, file_path)

            await FileRecord.create(original_name=file_name, file_hash=file_hash, file_type=file_type, file_path=file_path, source=source)
            return True
        except Exception as e:
            logger.error("upload file error", exc_info=e)
            return False
            
        
        
    