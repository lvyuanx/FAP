import importlib
import logging
import os

logger = logging.getLogger("faplus")

class ModuleLoader:
    def __init__(self, module_name="settings"):
        self.module_name = module_name
        self._settings = None  # 缓存模块

    def _load_settings(self):
        if self._settings is None:
            logger.debug("Loading settings...")
            self._settings = importlib.import_module(self.module_name)
        return self._settings

    def reload(self):
        """重新加载 settings 模块"""
        logger.debug("Reloading settings...")
        self._settings = importlib.reload(self._load_settings())

    def __getattr__(self, name):
        # 触发懒加载
        settings_module = self._load_settings()
        if hasattr(settings_module, name):
            return getattr(settings_module, name)
        raise AttributeError(f"'settings' object has no attribute '{name}'")


FAP_SETTINGS_MODULE = os.environ.get("FAP_SETTINGS_MODULE")

settings = ModuleLoader(FAP_SETTINGS_MODULE)  # settings.py 文件的模块名称


def import_status_code_enum():
    try:
        # 确保 settings.APPLIICATION_ROOT 是可信的
        application_root = settings.APPLICATION_ROOT
        if not application_root:
            raise ValueError("settings.APPLICATION_ROOT is not set or is empty")

        # 动态导入模块
        module_path = f"{application_root}.http_status_code"
        module = importlib.import_module(module_path)

        # 获取 StatusCodeEnum
        status_code_enum = getattr(module, 'StatusCodeEnum', None)
        if status_code_enum is None:
            raise AttributeError(f"Module {module_path} does not contain 'StatusCodeEnum'")
        
        return status_code_enum
    except (ImportError, AttributeError, ValueError) as e:
        raise RuntimeError(f"Failed to import StatusCodeEnum: {e}") from e

StatusCodeEnum = import_status_code_enum()