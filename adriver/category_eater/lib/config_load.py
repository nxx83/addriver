import logging
from logging.config import dictConfig
import sys

import os
from yaml import safe_load

logger = logging.getLogger(__name__)

ADRIVER_CONFIG_PATH = "/usr/local/rle/etc"


class ConfigLoader(object):

    def __init__(self, app_name, config_search_paths=None,
                 config_env_var=None, logging_env_var=None):

        self.app_name = app_name

        if config_search_paths is None:
            config_search_paths = [
                ".",
                os.path.join(ADRIVER_CONFIG_PATH, self.app_name.lower())
            ]
        self.config_search_paths = config_search_paths

        if config_env_var is None:
            config_env_var = "{}_CONFIG".format(self.app_name.upper())
        self.config_env_var = config_env_var

        if logging_env_var is None:
            logging_env_var = "{}_LOGGING_CONFIG".format(self.app_name.upper())
        self.logging_env_var = logging_env_var

    def get_path(self, file_name=None, env_var=None):
        file_path = None

        env_path = os.getenv(env_var, None)
        if env_path:
            file_path = env_path
        else:
            for path in self.config_search_paths:
                config_file_path = os.path.join(path, file_name)
                if os.path.isfile(config_file_path):
                    file_path = config_file_path

        return os.path.abspath(file_path) if file_path else None

    def load_config(self, file_path=None):

        if file_path:
            if not os.path.isfile(file_path):
                raise RuntimeError("File \"{}\" not found".format(file_path))
        else:
            file_path = self.get_path(
                file_name="config.yml",
                env_var=self.config_env_var
            )

            if not file_path:
                raise RuntimeError("Can not get config file location.")

        logger.info(
            "Configuration will be loaded from: \"{path}\"".format(
                path=file_path
            )
        )
        config = safe_load(open(file_path, 'r'))
        logger.info("Configuration loaded")

        return config

    def configure_logging(self, file_path=None):

        if file_path:
            if not os.path.isfile(file_path):
                raise RuntimeError("File \"{}\" not found".format(file_path))
        else:
            file_path = self.get_path(
                file_name="logger.yml",
                env_var=self.logging_env_var
            )

            if not file_path:
                raise RuntimeError("Can not get logging config file location.")

        dictConfig(safe_load(open(file_path, 'r')))
        logger.info("Logging config loaded from: \"{path}\"".format(
            path=file_path
        ))
