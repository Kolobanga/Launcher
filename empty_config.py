from config import Config


class EmptyConfig(Config):
    def __init__(self):
        super().__init__()
        self.setName('Default')
        self.addVersion('*')
        self.addFlag('cmd', '#string()', 'Commandline arguments')