# main/http_status_code.py
from enum import Enum
from faplus.http_status_code import StatusCodeEnum as SysCodeEnum
from faplus.auth.http_status_code import StatusCodeEnum as AuthCodeEnum


class MainCodeEnum(Enum):
    发送文本邮件失败 = "010000"
    站点配置不存在 = ("010100", "站点{name}配置不存在")
    站点邮件地址未配置 = ("010100", "站点{name}邮件地址未配置")


def merge_enums(*enums):
    # 创建一个新的字典，存储合并后的枚举成员
    merged_enum_dict = {}
    for enum in enums:
        for name, member in enum.__members__.items():
            merged_enum_dict[name] = member.value
    # 使用type动态创建一个新的枚举类
    return Enum("MergedStatusCodeEnum", merged_enum_dict)

# 动态合并枚举类
StatusCodeEnum = merge_enums(SysCodeEnum, AuthCodeEnum, MainCodeEnum)