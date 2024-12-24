from fastapi import Body
from chat.schemas import AuthenticateReq
from faplus.view import PostView
from chat.utils import chat_util
from faplus.utils import token_util

class View(PostView):

    finally_code = "00", "认证失败"
    status_codes = [
      ("01", "工单系统登录失败")  
    ]
    
    @staticmethod
    async def api(data: AuthenticateReq = Body()):
        """hello"""
        
        # 调用第三方登录接口
        res = await chat_util.authenticate_user(data.username, data.password)
        if not res:
            return View.make_code("01")
        username, uid = res
        token = token_util.create_token({"username": username, "uid": uid})
        return {"tk": token}
        