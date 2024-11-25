#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: close_info_shutdowns.py
Author: lvyuanxiang
Date: 2024/11/25 10:32:32
Description: 关闭信息
"""
import logging

logger = logging.getLogger(__package__)


def create_shutdown_event(**kwargs):
    async def print_info():
        logger.info("\n\n》》》》》》》》》》》》》》》》》》》》》》》》》 FastApi Plus 《《《《《《《《《《《《《《《《《《《《《《《《《\n\n")
    
    return print_info