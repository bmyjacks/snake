import configparser


class Config:
    def __init__(self, file='config.conf'):
        self._config = configparser.ConfigParser()
        self._config.read(file)

    def get(self, section, key):
        return self._config[section][key].strip("'").strip('"')

    def getboolean(self, section, key):
        return self._config.getboolean(section, key)

    def getint(self, section, key):
        return self._config.getint(section, key)
