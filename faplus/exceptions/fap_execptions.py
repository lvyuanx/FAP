#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: fap_execptions.py
Author: lvyuanxiang
Date: 2024/11/13 14:36:39
Description: FAP通用异常
"""

from faplus.utils.config_util import StatusCodeEnum


class FAPStatusCodeException(Exception):
    """FAP StatusCode通用异常基类"""

    def __init__(self, code: StatusCodeEnum, msg_dict: dict = None, data: dict = None) -> None:
        """
        初始化异常类

        :param code: 异常码
        :param msg_dict: 异常提示占位符数据, defaults to None
        :param data: 异常返回数据, defaults to None
        """
        msg = code.name
        super().__init__(msg)
        self.code = code
        self.msg_dict = msg_dict
        self.data = data
