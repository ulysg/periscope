import configparser

CONFIG_LOCATION = "config.ini"

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_LOCATION)

    def get(self, section: str, key: str) -> str:
        return self.config[section][key]

    def set(self, section: str, key: str, value: str):
        try:
            self.config[section][key] = value

        except KeyError:
            self.config[section] = {}
            self.config[section][key] = value

        with open(CONFIG_LOCATION, "w") as configfile:
            self.config.write(configfile)

config = Config()
