import sys
import os
import json

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *

from ArgumentsWidget import *


def getRootDir():
    return os.path.dirname(__file__)

configs = []
presets = []
applications = {}

def loadConfigs(configsFolder='./configs'):
    for file in os.listdir(configsFolder):
        if os.path.splitext(file)[-1].lower() == '.cfg':
            path = os.path.join(getRootDir(), 'configs', file)
            with open(path, 'rt') as f:
                j = json.load(f)
                versions = j['AppVersion']
            try:
                applications[j['AppName']] == None
            except KeyError:
                applications[j['AppName']] = []
            for version in versions:
                applications[j['AppName']].append(version)
            configs.append(j)

def loadPresets(presetsFolder='./presets'):
    for file in os.listdir(presetsFolder):
        if os.path.splitext(file)[-1].lower() == '.set':
            presets.append(os.path.splitext(file)[0])

if __name__ == '__main__':
    loadConfigs()
    print(configs)
    print(applications)
    loadPresets()
    print(presets)

def createNewPreset():
    pass

def launchApplication():
    if sys.platform.startswith('win'):
        os.system()
    elif sys.platform.startswith('linux'):
        pass
    elif sys.platform == 'darwin':
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('DCC Launcher')
        self.setMinimumSize(QSize(600, 400))
        self.resize(QSize(800, 500))

        # Central Widget
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # Main Menu
        self.mainMenu = QMenuBar()
        self.setMenuBar(self.mainMenu)

        self.appMenu = QMenu('Application')
        self.mainMenu.addMenu(self.appMenu)

        self.settingsAction = QAction('Settings', self)
        self.settingsAction.triggered.connect(self.callSettings)
        self.appMenu.addAction(self.settingsAction)

        self.appMenu.addSeparator()

        self.quitAction = QAction('Quit', self)
        self.quitAction.triggered.connect(lambda: app.exit(0))
        self.appMenu.addAction(self.quitAction)

        self.aboutMenu = QMenu('About')
        self.mainMenu.addMenu(self.aboutMenu)

        self.aboutMenu.addAction('About', self.callAbout)

        # Layouts
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        # self.topHorizontalLayout = QHBoxLayout()
        # self.verticalLayout.addLayout(self.topHorizontalLayout)
        self.middleHorizontalLayout = QHBoxLayout()
        self.verticalLayout.addLayout(self.middleHorizontalLayout)
        # Presets Widget
        self.presetList = QListWidget()
        self.presetList.setFixedWidth(130)
        self.middleHorizontalLayout.addWidget(self.presetList)
        self.rightMiddleLayout = QVBoxLayout()
        self.middleHorizontalLayout.addLayout(self.rightMiddleLayout)

        # Right Controls
        self.controlsLayout = QHBoxLayout()
        self.launchButton = QPushButton('Launch')
        self.launchButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.launchButton)
        self.createLinkButton = QPushButton('Create Link')
        self.createLinkButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.createLinkButton)
        self.newPresetButton = QPushButton('New Preset')
        self.newPresetButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.newPresetButton)
        self.saveButton = QPushButton('Save Preset')
        self.saveButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.saveButton)
        self.controlsSpacerItem = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.controlsLayout.addItem(self.controlsSpacerItem)
        self.rightMiddleLayout.addLayout(self.controlsLayout)

        # Tabs
        self.tabs = QTabWidget()
        self.rightMiddleLayout.addWidget(self.tabs)

        # Flags Tab
        self.flagsTab = QWidget()
        self.flagsTabMainLayout = QVBoxLayout(self.flagsTab)
        self.flagsTabTopLayout = QHBoxLayout()
        self.flagsTabMainLayout.addLayout(self.flagsTabTopLayout)
        self.tabs.addTab(self.flagsTab, 'Command line Flags')
        self.args = ArgumentsWidget()
        self.flagsTabMainLayout.addWidget(self.args)

        self.lab1 = QLabel('Application')
        self.comb1 = QComboBox()
        self.comb1.addItems(list(applications.keys()))  # To function
        self.comb1.currentTextChanged.connect(self.fillComb2)
        self.lab2 = QLabel('Version')
        self.comb2 = QComboBox()
        self.fillComb2()
        self.flagsTabTopSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.flagsTabTopLayout.addWidget(self.lab1)
        self.flagsTabTopLayout.addWidget(self.comb1)
        self.flagsTabTopLayout.addWidget(self.lab2)
        self.flagsTabTopLayout.addWidget(self.comb2)
        self.flagsTabTopLayout.addSpacerItem(self.flagsTabTopSpacer)


        # Environment Variables Tab
        self.envVarsTab = QWidget()
        self.envVarsTabMainLayout = QVBoxLayout(self.envVarsTab)
        self.vars = QTableWidget(1, 2)
        self.vars.setHorizontalHeaderLabels(['Variable', 'Value'])
        self.envVarsTabMainLayout.addWidget(self.vars)
        self.tabs.addTab(self.envVarsTab, 'Environment Variables')
        self.vars.verticalHeader().hide()
        self.vars.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Applications Tab
        self.appTab = QWidget()
        self.appTabMainLayout = QHBoxLayout(self.appTab)
        self.allAppsList = QListWidget()
        self.appTabMainLayout.addWidget(self.allAppsList)
        self.middleButtonsLayout = QVBoxLayout()
        self.appTabMainLayout.addLayout(self.middleButtonsLayout)
        self.middleButtonsSpacerTop = QSpacerItem(10, 10, QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.middleButtonsLayout.addSpacerItem(self.middleButtonsSpacerTop)
        self.middleButtonsSpacerBottom= QSpacerItem(10, 10, QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.moveAppRight = QPushButton('>>')
        self.moveAppRight.setFixedWidth(25)
        self.middleButtonsLayout.addWidget(self.moveAppRight)
        self.moveAppLeft = QPushButton('<<')
        self.moveAppLeft.setFixedWidth(25)
        self.middleButtonsLayout.addWidget(self.moveAppLeft)
        self.middleButtonsLayout.addSpacerItem(self.middleButtonsSpacerBottom)
        self.presetAppsList = QListWidget()
        self.appTabMainLayout.addWidget(self.presetAppsList)
        self.tabs.addTab(self.appTab, 'Applications')


        # houdini16_5 = {'AppName': 'Houdini',
        #           'AppVersion': ['16.0', '16.5'],
        #           'Flags': [{'Name': 'Foreground',
        #                      'Description': 'In Mac OS X and Linux, when you run Houdini from the command line, by default it "backgrounds" itself, returning control of the terminal to the shell. This option instead keeps Houdini in the "foreground", meaning you won’t be able to type more commands to the shell until Houdini exists or you press ⌃ Ctrl + Z to pause the foreground process.',
        #                      'Template': '-foreground'},
        #                     {'Name': 'Background',
        #                      'Description': 'Houdini will "background" itself after starting, returning control of the terminal to the shell. This is the default.',
        #                      'Template': '-background'},
        #                     {'Name': 'Geometry',
        #                      'Description': 'Define the window geometry on the screen (see also -span). For example\nhoudini -geometry=WxH+X+Y\n(where W is width, H is height, X is horizontal position, and Y is vertical position). The geometry specification cannot have spaces. X and Y may be negative (in which case you would use - instead of + as a separator). Some window managers do not allow larger windows than the screen, overlapping of manager toolbars, and/or positioning offscreen.',
        #                      'Template': '-geometry #int(Width) #int(Height)+#int(Left)+#int(Top)'},
        #                     {'Name': 'Manual Cook Mode',
        #                      'Description': 'Start Houdini in "manual" cook mode.',
        #                      'Template': '-n'},
        #                     {'Name': 'Span',
        #                      'Description': 'When you specify this option on a computer with multiple monitors, Houdini will start up spanning all monitors, so the main Houdini window fills them all (where possible, discounting resolution differences and non-rectangular layouts). This only works on some window managers, and has no effect in single-monitor setups. Cannot be used with -geometry.',
        #                      'Template': '-span'}]}
        # with open('struct.json', 'w') as file:
        #     json.dump(houdini16_5, file, indent=4)

        # self.fillPresetList()

    def fillComb2(self):
        self.comb2.clear()
        self.comb2.addItems(sorted(applications[self.comb1.currentText()], reverse=True))

    def callSettings(self):
        pass

    def callAbout(self):
        print('Python 3 / PyQt5')

    # def fillPresetList(self):
    #     for preset in scanPresetsFolder():
    #         item = QListWidgetItem(preset)
    #         self.presetList.addItem(item)

    def presetListMenu(self):
        menu = QMenu()
        ACTIONS = {'New preset':1}
        for a in ACTIONS:
            action = QAction(a)
            menu.addAction()
        menu.exec_(QCursor.pos())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    # Style
    # with open('style.qss', 'rt') as style:
    #     app.setStyleSheet(style.read())

    mainWindow.show()
    sys.exit(app.exec_())
