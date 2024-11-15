#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: init_api.py
Author: lvyuanxiang
Date: 2024/11/06 11:48:48
Description: 程序入口
"""
import os
import logging
import argparse
import importlib
import asyncio

import uvicorn
from fastapi.applications import FastAPI


logger = logging.getLogger("FastApiPlus")


class FastApiPlusApplication(object):

    app: FastAPI = None

    def __init__(self) -> None:
        os.environ.setdefault("FAP_PACKAGE", __package__)
        # 初始化logging
        self.get_args()

    def execute_command(self, args: argparse.Namespace):
        """执行命令行参数"""
        command_dict = {
            "runserver": self.runserver,
            "migrations": self.migrations,
            "init_db": self.init_db,
            "migrate": self.migrate,
            "downgrade": self.downgrade,
            "history": self.history,
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

        # runserver
        parser_runserver = subparsers.add_parser("runserver", help="启动服务器")
        parser_runserver.add_argument(
            "--host_port", type=str, default="0.0.0.0:8848", help="指定服务器监听的 host 和 port，格式如 0.0.0.0:8000")
        parser_runserver.add_argument(
            "--reload", action="store_true", help="是否开启热加载模式")
        parser_runserver.add_argument("--workers", type=int, help="指定工作进程数")
        
        # migrations
        subparsers.add_parser("migrations", help="生成数据库迁移文件")

        # init db
        subparsers.add_parser("init_db", help="初始化数据库")
        
        # migrate
        subparsers.add_parser("migrate", help="执行数据库迁移")
        
        # history
        subparsers.add_parser("history", help="查看数据库迁移历史")
        
        # downgrade
        parser_downgrade = subparsers.add_parser("downgrade", help="回滚数据库迁移")
        parser_downgrade.add_argument("--version", type=str, help="回滚版本")
        
        
        args = parser.parse_args()
        self.execute_command(args)

    def load(self):
        """系统中的功能使用loader进行加载"""
        package = __package__
        loader_lst = [
            "logging_loader",
            "router_loader",
            "tortoise_loader",
        ]
        try:
            for loader in loader_lst:
                loader_module = importlib.import_module(f"{package}.loaders.{loader}")
                res = getattr(loader_module, "loader")(self.app)
                if res and isinstance(res, FastAPI):
                    self.app = res
        except Exception as e:
            logger.error("fast api plus load error", exc_info=True)
            raise e
    
    def event_register(self, app: FastAPI):
        """事件注册"""
        from . import settings
        startups: list[str] = getattr(settings, "FAP_STARTUPS", [])
        shutdowns: list[str] = getattr(settings, "FAP_SHUTDOWNS", [])
        logger.debug("fast api plus startup -> {startups}")
        logger.debug("fast api plus shutdown -> {shutdowns}")
        def add_event(event: str, func_path: str):
            path, func_name = func_path.rsplit(".", 1)
            module = importlib.import_module(path)
            func = getattr(module, func_name, None)
            assert callable(func), f"{func_path} is not callable"
            assert asyncio.iscoroutinefunction(func), f"{func_path} is not a coroutine function"
            app.add_event_handler(event, func)
        
        for startup in startups:
            add_event("startup", startup)
        
        for shutdown in shutdowns:
            add_event("shutdown", shutdown)

                              

    def runserver(self, command_args: argparse.Namespace):
        """启动服务器"""
        # 加载功能模块
        self.load()

        app = self.app
        if not app:
            raise RuntimeError("application is None")
        
        # 注册事件
        self.event_register(app)

        # 启动服务
        host, port = command_args.host_port.split(":")
        uvicorn.run(app, host=host, port=int(port),
                    reload=command_args.reload, workers=command_args.workers)
    
    
    def run_cmd(self, cmd: str):
        import subprocess
        subprocess.run(cmd, shell=True)
    
    
    def migrations(self, command_args: argparse.Namespace):
        self.run_cmd(f"aerich init -t {__package__}.orm.tortoise.TORTOISE_ORM")
    
    def init_db(self, command_args: argparse.Namespace):
        self.run_cmd("aerich init-db")
    
    def migrate(self, command_args: argparse.Namespace):
        self.run_cmd("aerich migrate")
        self.run_cmd("aerich upgrade")
    
    
    def downgrade(self, command_args: argparse.Namespace):
        version = command_args.version
        self.run_cmd(f"aerich downgrade -v {version} -d")
    
    def history(self, command_args: argparse):
        self.run_cmd("aerich downgrade --help")
        