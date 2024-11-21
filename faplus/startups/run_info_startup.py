import logging

from datetime import datetime, time
from faplus import settings, dft_settings

logger = logging.getLogger(__package__)


split_line = "#" * 30 + " FastApi Plus " + "#" * 30

print_template = "\n\n" + split_line + """

FastApi Plus Runserver, Version: {version}, time: {time}
{cmd_args.host_port}  reload {cmd_args.reload}  workers {cmd_args.workers}

推荐使用在线文档进行接口调试
redocs: http://{cmd_args.host_port}{redoc_url}
docs: http://{cmd_args.host_port}{docs_url}

""" + split_line + "\n\n"


def create_startup_event(**kwargs):
    async def print_info():
        cmd_args = kwargs.get("cmd_args", None)
        DEBUG = getattr(settings, "DEBUG", dft_settings.DEBUG)
        if not cmd_args or not DEBUG:
            return

        FAP_REDOC_URL = getattr(settings, "FAP_REDOC_URL",
                                dft_settings.FAP_REDOC_URL)
        FAP_DOCS_URL = getattr(settings, "FAP_DOCS_URL",
                               dft_settings.FAP_DOCS_URL)
        FAP_VERSION = getattr(settings, "FAP_VERSION",
                              dft_settings.FAP_VERSION)
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(print_template.format(cmd_args=cmd_args, redoc_url=FAP_REDOC_URL,
                    docs_url=FAP_DOCS_URL, time=time_str, version=FAP_VERSION))

    return print_info
