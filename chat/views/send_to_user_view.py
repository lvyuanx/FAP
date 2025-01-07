from fastapi import Body, Header
from chat.schemas import SendToUserReq
from faplus.view import PostView
from chat.utils import chat_util
from faplus.utils import settings
from chat import const

class View(PostView):

    finally_code = "00", "消息发送失败"

    @staticmethod
    async def api(authorization: str = Header(None, description="登录token", alias=settings.GONGDAN_TK_FLAG), data: SendToUserReq = Body()):

        await chat_util.send_to(data.users, {"code": const.WS_MSG_OPEN_URL_CODE, "data": data.msg.dict()})
