

import importlib
import logging
from typing import Dict

from fastapi import WebSocket


from faplus.websocket.route_base import RouteBase

logger = logging.getLogger(__package__)


# 存储所有活跃的 WebSocket 连接
active_connections: Dict[str, WebSocket] = {}

class WSChatRoute(RouteBase):
    
    url = "/ws"
    user_class = "chat.chat_user.WSChatUser"

    async def endpoint(self, websocket: WebSocket):
        path, name = self.user_class.rsplit(".", 1) 
        user_module = importlib.import_module(path)
        user_class = getattr(user_module, name)
        user = user_class()
        await user.run(websocket)
