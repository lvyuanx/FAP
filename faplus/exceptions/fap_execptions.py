#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: fap_execptions.py
Author: lvyuanxiang
Date: 2024/11/13 14:36:39
Description: FAP通用异常
"""

class FAPException(Exception):
    """FAP 通用异常基类"""
    
    def __init__(self, msg="FAP execption", code=None, data=None) -> None:
        super().__init__(msg)
        self.msg = msg
        self.code = code
        self.data = data