from PyQt5.QtWidgets import qApp

from default_config import DefaultConfig
from serialization import Serialization


class Preset(Serialization):
    def __init__(self, config=DefaultConfig()):
        self.__name = None
        self.__config = config
        self.__file = None
        self.__flags = {}  # {'Name': [values, ...]}  # Todo: {} instead []
        self.__vars = {}
        self.__apps = set()

    def addApplication(self, link):
        self.__apps.add(link)

    def applications(self):
        return self.__apps

    def compileArgs(self):
        return ''

    def setName(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def setConfig(self):
        raise NotImplementedError

    def config(self):
        return self.__config

    def setFile(self, link):
        self.__file = link

    def file(self):
        return self.__file

    def setFlag(self, name, values):
        self.__flags[name] = values

    def removeFlag(self, name):
        del self.__flags[name]

    def setVariable(self, name, value):
        self.__vars[name] = value

    def variable(self, name):
        return self.__vars[name]

    def variables(self):
        return self.__vars

    def removeVariable(self, name):
        if name in self.__vars:
            del self.__vars[name]

    def serialize(self):
        data = {'Name': self.__name,
                'Config': self.__config.name(),
                'Flags': self.__flags,
                'Vars': self.__vars}
        return super().serialize(data)

    def deserialize(self, data, link):
        self.__name = data.get('Name')
        self.setFile(link)
        self.__config = qApp.configs.get(data.get('Config'))
        self.__flags = data.get('Flags')
        self.__vars = data.get('Vars')
        return super().deserialize(data)
