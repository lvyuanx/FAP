import logging

from fastapi import Body

from faplus.view import PostView, Response, StatusCodeEnum
from faplus import settings
from mail.schemas import SendErrorMailReqSchema


from mail.utils import mail_util

# 站点配置
SITE_CONFIG = settings.SITE_CONFIG
# 转发邮件的用户
MAIL_USER = settings.MAIL_USER


logger = logging.getLogger("sys")


class View(PostView):
    
    finally_code = StatusCodeEnum.发送文本邮件失败

    
    
    @staticmethod
    async def api(data: SendErrorMailReqSchema = Body(..., description="错误邮件请求的数据"),):
        """发送错误栈邮件"""
        if data.site_name not in SITE_CONFIG:
            return Response.FAIL(
                StatusCodeEnum.站点配置不存在, msg_dict={"name": data.site_name}
            )
        to_users = SITE_CONFIG[data.site_name].get("mails", [])
        if len(to_users) < 1:
            return Response.FAIL(
                StatusCodeEnum.站点邮件地址未配置, msg_dict={"name": data.site_name}
            )
        send_data = {
            "to_user": ",".join(to_users),
            "from_user": MAIL_USER,
            "subject": f"{data.site_name}发生错误：{data.error_msg}",
            "message": data.traceback,
            "level": data.level,
        }
        mail_util.send_text_mail(**send_data)

