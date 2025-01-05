from mail.apis import apis as MAIL_APIS
from faplus.auth.apis import apis as AUTH_APIS
from faplus.media.apis import apis as MEDIA_APIS


apis = [
    ("10", "", AUTH_APIS, "认证模块"),
    ("11", "/mail", MAIL_APIS, "邮件服务"),
    ("12", "/media", MEDIA_APIS, "媒体服务"),
]
