import fastapi
from tortoise.contrib.fastapi import register_tortoise

from ..orm.tortoise import GENERATE_SCHEMAS, DEBUG, TORTOISE_ORM, ENGINE


def loader(app: fastapi):
    """初始化数据库"""
    if ENGINE:
        register_tortoise(app, config=TORTOISE_ORM, generate_schemas=GENERATE_SCHEMAS, add_exception_handlers=DEBUG)