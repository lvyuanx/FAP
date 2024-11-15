# -*- coding: utf-8 -*-

import logging.config
import os

from faplus.utils.config_util import settings


def load_logging_cfg():
    log_level = getattr(settings, "LOG_LEVEL", "DEBUG")
    log_dir = getattr(settings, "LOG_DIR", "logs")
    logging_cfg = getattr(settings, "LOGGING", None)
    
    assert log_level.upper() in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), \
        f"logger level mast be DEBUG, INFO, WARNING, ERROR, CRITICAL, but got {log_level}"
    
    assert log_dir and os.path.isdir(log_dir), \
        f"log_dir must be a valid directory path, but got {log_dir}"
        
    assert logging_cfg is None or isinstance(logging_cfg, dict), \
        "logging_cfg must be a dict, but got {}".format(type(logging_cfg))

    if not logging_cfg:
        logging_cfg = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": "[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
                },
                "simple": {
                    "format": "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
                },
            },
            "handlers": {
                "all": {  # 记录所有日志
                    "level": "DEBUG",
                    "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
                    "file_path": log_dir,
                    "suffix": "%Y-%m-%d-all",
                    "formatter": "detailed",
                    "backup_count": 30,
                    "encoding": "utf-8",
                },
                "project": {  # 记录项目日志
                    "level": "DEBUG",
                    "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
                    "file_path": log_dir,
                    "suffix": "%Y-%m-%d-project",
                    "formatter": "detailed",
                    "backup_count": 30,
                    "encoding": "utf-8",
                },
                "error": {  # 只记录错误日志
                    "level": "ERROR",
                    "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
                    "file_path": log_dir,
                    "suffix": "%Y-%m-%d-error",
                    "formatter": "detailed",
                    "backup_count": 30,
                    "encoding": "utf-8",
                },
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["all", "console", "error"],
                    "level": log_level,
                    "propagate": True,
                },
                "sys": {"handlers": ["project"], "level": log_level},
            },
        }
    
    return logging_cfg


def init_logging():
    
    # 加载配置
    logging.config.dictConfig(load_logging_cfg())
