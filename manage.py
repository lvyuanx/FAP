#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: manage.py
Author: lvyuanxiang
Date: 2024/11/12 16:59:29
Description: FAP项目启动入口
"""


import os


if __name__ == '__main__':
    os.environ.setdefault("FAP_SETTINGS_MODULE", "main.settings")
    from faplus.management import execute_from_command_line
    execute_from_command_line()
