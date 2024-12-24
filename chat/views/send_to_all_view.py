from fastapi import Body, Header
from faplus.view import PostView
from chat.utils import chat_util
from chat.schemas import OpenUrlMsg
from chat import const

class View(PostView):

    finally_code = "00", "消息发送失败"
    
    @staticmethod
    async def api(authorization: str = Header(None, description="登录token"), msg: OpenUrlMsg = Body(description="消息内容")):
        await chat_util.send_all({"code": const.WS_MSG_OPEN_URL_CODE, "data": msg.dict()})