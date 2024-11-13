from pydantic import Field, BaseModel

from mail.const import MailLevelEnum




class SendTextMailReqSchema(BaseModel):
    """请求发送邮件的参数"""

    to_user: str = Field(description="收件人")
    from_user: str = Field(description="发件人")
    msg: str = Field(description="邮件内容")
    subject: str = Field(description="邮件主题")
    level: MailLevelEnum = Field(description="日志级别， 1：普通，2：一般，3：严重")


class SendErrorMailReqSchema(BaseModel):
    """请求发送错误邮件的参数"""

    site_name: str = Field(description="站点名称: open_shengfy, pis, watch_inteface")
    error_msg: str = Field(description="错误msg")
    traceback: str = Field(description="错误堆栈信息")
    level: MailLevelEnum = Field(description="日志级别， 1：普通，2：一般，3：严重")