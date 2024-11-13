#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: init_api.py
Author: lvyuanxiang
Date: 2024/11/06 11:48:48
Description: 程序入口
"""
import logging
import argparse

import uvicorn
from fastapi.applications import FastAPI


logger = logging.getLogger("FastApiPlus")


class FastApiPlusApplication(object):

    app: FastAPI = None

    def __init__(self) -> None:
        # 初始化logging
        self.get_args()

    def execute_command(self, args: argparse.Namespace):
        """执行命令行参数"""
        command_dict = {
            "runserver": self.runserver
        }

        if args.command in command_dict:
            command_dict[args.command](args)
        else:
            raise RuntimeError("command not found")

    def get_args(self):
        """获取命令行参数"""
        parser = argparse.ArgumentParser(
            description="FastApiPlus 启动参数"
        )
        # 创建子解析器，用于管理子命令
        subparsers = parser.add_subparsers(dest="command", help="子命令")
        # runserver 子命令
        parser_runserver = subparsers.add_parser("runserver", help="启动服务器")
        parser_runserver.add_argument(
            "--host_port", type=str, default="0.0.0.0:8848", help="指定服务器监听的 host 和 port，格式如 0.0.0.0:8000")
        parser_runserver.add_argument(
            "--reload", action="store_true", help="是否开启热加载模式")
        parser_runserver.add_argument("--workers", type=int, help="指定工作进程数")

        args = parser.parse_args()
        self.execute_command(args)

    def load(self):
        """系统中的功能使用loader进行加载"""
        from .loaders import router_loader, logging_loader
        loader_lst = [
            logging_loader,
            router_loader
        ]
        try:
            for loader in loader_lst:
                res = loader.loader()
                if res and isinstance(res, FastAPI):
                    self.app = res
        except Exception as e:
            logger.error("fast api plus load error", exc_info=True)
            raise e

    def runserver(self, command_args: argparse.Namespace):
        """启动服务器"""
        # 加载功能模块
        self.load()

        app = self.app
        if not app:
            raise RuntimeError("application is None")

        # 启动服务
        host, port = command_args.host_port.split(":")
        uvicorn.run(app, host=host, port=int(port),
                    reload=command_args.reload, workers=command_args.workers)
