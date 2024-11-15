from .views import send_text_mail_view, send_error_mail_view

apis = {
    "/text": [
        ("00", "/send", send_text_mail_view, "发送文本类型的邮件")
    ],
    "/error": [
        ("01", "/send", send_error_mail_view, "发送错误类型的邮件")
    ]
}