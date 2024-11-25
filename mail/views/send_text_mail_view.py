from faplus.view import PostView, logger, Response, StatusCodeEnum
from mail.schemas import SendTextMailReqSchema


from mail.utils import mail_util


class View(PostView):

    finally_code = ("00", "发送文本邮件失败")

    @staticmethod
    async def api(data: SendTextMailReqSchema):
        mail_util.send_text_mail(
            to_user=data.to_user,
            from_user=data.from_user,
            subject=data.subject,
            message=data.msg,
            level=data.level,
        )
