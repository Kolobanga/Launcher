import json


class Serialization:
    def serialize(self, data):
        return data

    def deserialize(self, data):
        return self

    def saveToFile(self, filename):
        try:
            data = json.dumps(self.serialize(), ensure_ascii=False, indent=4, sort_keys=False)
            with open(filename, 'wt', encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            print('Saving error:', str(e))

    def loadFromFile(self, filename):
        with open(filename, 'rt', encoding='utf-8') as file:
            return self.deserialize(json.load(file), filename)
