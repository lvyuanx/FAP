

import logging
from urllib.parse import parse_qs, urlparse

from fastapi import WebSocket
from fastapi import WebSocket, WebSocketDisconnect

from faplus.websocket.user_base import UserBase
from chat.chat_route import active_connections
from faplus.utils import token_util

logger = logging.getLogger(__package__)

class WSChatUser(UserBase):
    
    url = "/ws"
    room_cache_key = "chat"

    def authenticate_user(self, websocket: WebSocket):
        try:
            parsed_url = urlparse(str(websocket.url))
            query_params = parse_qs(parsed_url.query)
            tk = query_params.get("tk", [None])[0]
            if not tk:
                return None
            return token_util.verify_token(tk)
        except Exception as e:
            logger.error("Authenticate_user error", exc_info=True)
        
        return None
        

    async def join(self, websocket: WebSocket):
        user = self.authenticate_user(websocket)
        if not user:
            logger.error("websocket close")
            raise WebSocketDisconnect(code=1008)
        await websocket.accept()
        active_connections[user["uid"]] = websocket
        self.user = user["uid"]
    
    async def exit(self, websocket: WebSocket):
        active_connections.pop(self.user)
        
    
    async def handle_1(self, websocket: WebSocket, data: str):
        await websocket.send_text(f"Hello {data}!")
    
    async def handle_2(self, websocket: WebSocket, data: str):
        forward_user = active_connections.get(data)
        if forward_user:
            await forward_user.send_text(f"{self.user} forward to you")
        else:
            await websocket.send_text(f"user {data} not found")
