from serialization import Serialization


class Config(Serialization):
    def __init__(self):
        self.__name = None
        self.__flags = {}
        self.__file = None

    def clear(self):
        super(Config, self).__init__()

    def setName(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def addFlag(self, name, template, description=''):
        self.__flags[name] = {'Name:': name, 'Template': template, 'Description': description}

    def removeFlag(self, name):
        if name in self.__flags:
            del self.__flags[name]

    def flags(self):
        return self.__flags

    def setFile(self, link):
        self.__file = link

    def file(self):
        return self.__file

    def serialize(self):
        flags = [{'Name': name, 'Description': desc_temp[0], 'Template': desc_temp[1]} for name, desc_temp in
                 self.__flags.items()]
        data = {'AppName': self.__name,
                'Flags': flags}  # Todo: check
        return super().serialize(data)

    def deserialize(self, data, link):
        self.__name = data.get('AppName')
        self.setFile(link)
        for flag in data.get('Flags'):
            self.__flags[flag.get('Name')] = flag
        return super().deserialize(data)
