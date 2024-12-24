from pydantic import Field, BaseModel

from faplus.auth.views import user


class OpenUrlMsg(BaseModel):
    title: str = Field(description="标题")
    msg: str = Field(description="内容")
    url: str | None = Field(description="链接地址")

class SendToUserReq(BaseModel):
    """发送指定用户消息体"""
    
    users: list[str] = Field(description="用户邮箱列表")
    msg: OpenUrlMsg = Field(description="消息内容")


class SendBatchItemReq(BaseModel):
    """批量发送消息体项"""
    
    user: str = Field(description="用户邮箱")
    msg: OpenUrlMsg = Field(description="消息内容")

class AuthenticateReq(BaseModel):
    """批量发送消息体项"""
    
    username: str = Field(description="用户名")
    password: str = Field(description="密码")