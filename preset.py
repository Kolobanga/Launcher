from empty_config import EmptyConfig
from serialization import Serialization


class Preset(Serialization):
    def __init__(self, config=EmptyConfig()):
        self.__name = None
        self.__version = None
        self.__file = None
        self.__flags = {}  # {'Name': [values, ...]}

    def setName(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def setVersion(self, version):
        self.__version = str(version)

    def version(self):
        return self.__version

    def file(self):
        return self.__file

    def setFlag(self, name, values):
        self.__flags[name] = values

    def removeFlag(self, name):
        del self.__flags[name]

    def serialize(self):
        data = {'Name': self.__name,
                'Version': self.__version,
                'Flags': self.__flags}
        return super().serialize(data)

    def deserialize(self, data):
        self.__name = data['Name']
        self.__version = data['Version']
        self.__flags = data['Flags']
        return super().deserialize(data)