from enum import Enum


class CommonStatusCodeEnum(Enum):
    
    请求成功 = "0"
    请求失败 = "1"
    接口未实现 = "2"
    请求不存在 = "404"
