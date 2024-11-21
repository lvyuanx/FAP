from pydantic import Field, BaseModel
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    nickname: str | None = None
    email: str | None = None
    mobile: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class LoginReqSchema(BaseModel):
    """登录请求参数"""

    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    
class CreateUserReqSchema(BaseModel):
    """创建用户请求参数"""

    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    nickname: str | None = Field(description="昵称")
    email: str | None = Field(description="邮箱")
    mobile: str | None = Field(description="手机号码")
    is_superuser: bool = Field(description="是否是超级管理员")
    is_active: bool = Field(description="是否激活")