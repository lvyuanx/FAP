

from enum import Enum


class StatusCodeEnum(Enum):
    
    请求成功 = "0"
    请求失败 = "1"
    接口未实现 = "2"
    
    # ###################mail模块代码 01###################
    # 发送文本邮件代码 00
    发送文本邮件失败 = "010000"
    
    # 发送错误栈邮件代码 01
    站点配置不存在 = ("010100", "站点{name}配置不存在")
    站点邮件地址未配置 = ("010100", "站点{name}邮件地址未配置")
    
    # ###################权限模块代码 02###################
    # rsa加密代码 00
    RSA加密失败 = "020000"
    
    # rsa解密代码 01
    RSA解密失败 = "020100"
    
    # AES加密代码 02
    AES加密失败 = "020200"
    
    # AES解密代码 03
    AES解密失败 = "020300"
    
    # MD5加密代码 04
    MD5加密失败 = "020400"

    
    @staticmethod
    def get_by_code(code: str) -> "StatusCodeEnum":
        for status_code in StatusCodeEnum:
            val = status_code.value
            if isinstance(val, str):
                if val == code:
                    return status_code
            else:
                if code == val[0]:
                    return status_code
        raise ValueError(f"status code {code} not found")
