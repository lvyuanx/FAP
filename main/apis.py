from mail.apis import apis as MAIL_APIS
from faplus.auth.apis import apis as AUTH_APIS

apis = [
    ("01", "/mail", MAIL_APIS, "邮件服务"),
    ("02", "/auth", AUTH_APIS, "认证模块"),
]