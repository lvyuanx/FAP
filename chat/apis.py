from chat.views import send_to_all_view, send_to_user_view, send_batch_view, authenticate_view
from faplus.auth.views.encrypt_decrypt import aes_encrypt_view
apis = {
    "/auth": [
        ("03", "", authenticate_view, "认证"),
        ("04", "/tk", aes_encrypt_view, "创建token"),
    ],
    "/send": [
        ("00", "", send_to_user_view, "给指定用户推送消息"),
        ("01", "/all", send_to_all_view, "给所有用户推送消息"),
        ("02", "/batch", send_batch_view, "批量推送消息"),
    ]
}
