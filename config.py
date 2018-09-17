from serialization import Serialization


class Config(Serialization):
    def __init__(self):
        self.__name = None
        self.__versions = []
        self.__flags = {}

    def clear(self):
        super(Config, self).__init__()

    def setName(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def addVersion(self, version):
        self.__versions.append(str(version))

    def removeVersion(self, version):
        self.__versions.remove(str(version))

    def versions(self):
        return self.__versions

    def addFlag(self, name, template, description=''):
        self.__flags[name] = [template, description]

    def removeFlag(self, name):
        if name in self.__flags:
            del self.__flags[name]

    def flags(self):
        return self.__flags

    def serialize(self):
        data = {'AppName': self.__name,
                'AppVersion': self.__versions,
                'Flags': [{'Name': name, 'Description': desc_temp[0], 'Template': desc_temp[1]} for name, desc_temp in self.__flags.items()]}
        return super().serialize(data)

    def deserialize(self, data):
        self.__name = data.get('AppName')
        self.__versions = data.get('AppVersion')
        for flag in data.get('Flags'):
            self.__flags[flag.get('Name')] = [flag.get('Template'), flag.get('Description')]
        return super().deserialize(data)
