from fastapi import APIRouter
from .views.send_text_mail_view import View as SendTextMailView
from .views.send_error_mail_view import api as error_api

api = APIRouter()

# ******************************接口注册***************************************
# api.include_router(router=send_api, prefix="/text") # 发送文本邮件 00
api.include_router(router=SendTextMailView.router, prefix="/text") # 发送文本邮件 00
api.include_router(router=error_api, prefix="/error") # 发送错误栈邮件 01