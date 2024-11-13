from core.faplus.view import PostView, logger, Response, StatusCodeEnum
from mail.schemas import SendTextMailReqSchema


from mail.utils import mail_util


class View(PostView):
    
    name = "发送文本邮件"
    
    
    @staticmethod
    async def api(data: SendTextMailReqSchema):
        try:
            mail_util.send_text_mail(
                to_user=data.to_user,
                from_user=data.from_user,
                subject=data.subject,
                message=data.msg,
                level=data.level,
            )
        except Exception as e:
            logger.error("", exc_info=True)
            return Response.FAIL(StatusCodeEnum.发送文本邮件失败)

        return Response.OK()
    
    
    
