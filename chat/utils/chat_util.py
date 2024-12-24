import logging
from typing import Tuple
import json
import aiohttp
from aiohttp.typedefs import Query

from chat.chat_route import active_connections
from faplus import settings


logger = logging.getLogger(__package__)

async def send_all(msg: str | dict):
    """给所有用户发送消息"""
    if isinstance(msg, dict):
        msg = json.dumps(msg)
    for conn in active_connections.values():
        await conn.send_text(msg)

async def send_to(emails: list[str], msg: str | dict):
    """给指定用户发送消息"""
    for email, conn in active_connections.items():
        if email not in emails:
            break
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        await conn.send_text(msg)


async def send_batch(data: list[Tuple[str, str]]):
    """批量发送消息"""
    for email, msg in data:
        conn = active_connections.get(email)
        if not conn:
            logger.error(f"{email} not found")
            continue
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        await conn.send_text(msg)

async def authenticate_user(username: str, password: str):
    url = settings.GONDAN_LOGIN
    data = {
        "userName": username,
        "passWord": password
    }
    try:
    
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=data) as response:
                if response.status == 200:
                    result = await response.json()
                    data = result["data"]
                    return data["name"], data["userId"]
                else:
                    logger.error(f"Authentication failed with status {response.status}")
                    return None
    except Exception as e:
        logger.error("Authenticate_user error", exc_info=True)
        return None