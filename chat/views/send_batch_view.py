from fastapi import Body,Header
from chat.schemas import SendBatchItemReq
from faplus.view import PostView
from chat.utils import chat_util
from chat import const

class View(PostView):

    finally_code = "00", "批量发送消息失败"
    
    @staticmethod
    async def api(authorization: str = Header(None, description="登录token"), data: list[SendBatchItemReq] = Body()):
        """hello"""
        lst = []
        for item in data:
            lst.append((item.user, {"code": const.WS_MSG_OPEN_URL_CODE, "data": item.msg.dict()}))
        await chat_util.send_batch(lst)