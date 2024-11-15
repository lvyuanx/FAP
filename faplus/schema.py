from pydantic import BaseModel, Field
from typing import Optional, Union


class ResponseSchema(BaseModel):
    """请求返回格式"""

    code: str = Field(description="状态码")
    msg: Optional[str] = Field(description="状态信息")
    data: Optional[Union[dict, str]] = Field(description="返回数据")
