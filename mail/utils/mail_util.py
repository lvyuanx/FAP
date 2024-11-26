# coding:utf -8

import logging
import smtplib  # smtp服务器
from email.mime.text import MIMEText

from faplus.utils.config_util import settings
from mail.const import MailLevelEnum

logger = logging.getLogger(__package__)

MAIL_HOST = settings.MAIL_HOST
MAIL_PORT = settings.MAIL_PORT
MAIL_USER = settings.MAIL_USER
MAIL_PASSWORD = settings.MAIL_PASSWORD


msg_text_template = """<h1 style="color:{title_color};">{title}</h1>
{content}
"""

title_color_dict = {
    MailLevelEnum.NORMAL: "#000000",
    MailLevelEnum.MODERATE: "#FFA500",
    MailLevelEnum.SEVERE: "#FF0000",
}

title_level_str_dict = {
    MailLevelEnum.NORMAL: "普通",
    MailLevelEnum.MODERATE: "一般",
    MailLevelEnum.SEVERE: "严重",
}


def send_text_mail(
    to_user: str, from_user: str, subject: str, message: str, level: MailLevelEnum
):
    level_str = title_level_str_dict[level]
    return send_mail(
        to_user=to_user,
        from_user=from_user,
        subject=f"({level_str}) {subject}",
        message=message,
        level=level,
        template=msg_text_template,
    )


def send_mail(
    to_user: str,
    from_user: str,
    subject: str,
    message: str,
    level: MailLevelEnum,
    template: str,
):
    """
    发送邮件
    :param to: 收件人
    :param from: 发件人
    :param subject: 邮件主题
    :param message: 邮件内容
    :param level: 邮件级别
    :param template: 邮件模板
    :return:
    """
    message_html = template.format(
        title=subject, content=message, title_color=title_color_dict[level]
    )
    message = MIMEText(message_html, "html", "utf-8")
    message["Subject"] = subject
    message["To"] = to_user
    message["From"] = from_user

    smtp = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)  # 实例化smtp服务器
    smtp.login(MAIL_USER, MAIL_PASSWORD)  # 发件人登录
    smtp.sendmail(MAIL_USER, to_user, message.as_string())
    smtp.close()
    logger.info(
        f"[send success] - [{from_user}->{to_user}] : {subject} - {message}"
    )
    
