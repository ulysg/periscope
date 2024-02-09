import configparser
import os
import xdg_base_dirs

CONFIG_NAME = "config.ini"

class Config:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read(self._get_config_path())

    def get(self, section: str, key: str) -> str:
        return self._config[section][key]

    def set(self, section: str, key: str, value: str):
        try:
            self._config[section][key] = value

        except KeyError:
            self._config[section] = {}
            self._config[section][key] = value

        with open(self._get_config_path(), "w") as configfile:
            self._config.write(configfile)

    def _get_config_path(self):
        return os.path.join(xdg_base_dirs.xdg_config_home(), CONFIG_NAME)

config = Config()
