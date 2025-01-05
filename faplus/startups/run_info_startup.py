import logging

from datetime import datetime
from faplus import FastApiPlusApplication, get_setting_with_default

logger = logging.getLogger(__package__)


split_line = "#" * 30 + " FastApi Plus " + "#" * 30

print_template = (
    "\n\n"
    + split_line
    + """

FastApi Plus Runserver, Version: {version}, time: {time}
{cmd_args.host_port}  reload {cmd_args.reload}  workers {cmd_args.workers}

推荐使用在线文档进行接口调试
redocs: http://{cmd_args.host_port}{redoc_url}
docs: http://{cmd_args.host_port}{docs_url}

"""
    + split_line
    + "\n\n"
)


def run_info_event(**kwargs):
    async def do():
        DEBUG = get_setting_with_default("DEBUG")
        if not DEBUG:
            return

        cmd_args = FastApiPlusApplication.cmd_args

        FAP_REDOC_URL = get_setting_with_default("FAP_REDOC_URL")
        FAP_DOCS_URL = get_setting_with_default("FAP_DOCS_URL")
        FAP_VERSION = get_setting_with_default("FAP_VERSION")
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            print_template.format(
                cmd_args=cmd_args,
                redoc_url=FAP_REDOC_URL,
                docs_url=FAP_DOCS_URL,
                time=time_str,
                version=FAP_VERSION,
            )
        )

    return do
