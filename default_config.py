from config import Config


class DefaultConfig(Config):
    def __init__(self):
        super().__init__()
        self.setName('Default')
        self.addFlag('cmd', '#string()', 'Commandline arguments')
