import json
import os
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *

from arguments_widget import ArgumentsWidget


def rootDir():
    return os.path.dirname(__file__)


def homeDir():
    raise NotImplementedError


def isWindowsOS():
    return sys.platform.startswith('win')


def isLinuxOS():
    return sys.platform.startswith('linux')


def isMacOS():
    return sys.platform == 'darwin'


configs = []
presets = []
applications = {}


def loadConfigs(configsFolder='./configs'):
    for file in os.listdir(configsFolder):
        if os.path.splitext(file)[-1].lower() == '.cfg':
            path = os.path.join(rootDir(), 'configs', file)
            with open(path, 'rt') as f:
                data = json.load(f)
                versions = data['AppVersion']
            try:
                applications[data['AppName']] == None
            except KeyError:
                applications[data['AppName']] = []
            for version in versions:
                applications[data['AppName']].append(version)
            configs.append(data)


def loadPresets(presetsFolder='./presets'):
    for file in os.listdir(presetsFolder):
        if os.path.splitext(file)[-1].lower() == '.set':
            presets.append(os.path.splitext(file)[0])
    return presets


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


def createWindowsShortcut(targetLink, path, name, workDir):
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
        self.settingsAction.triggered.connect(self.settings)
        self.appMenu.addAction(self.settingsAction)

        self.appMenu.addSeparator()

        self.quitAction = QAction('Quit', self)
        self.quitAction.triggered.connect(lambda: qApp.exit(0))
        self.appMenu.addAction(self.quitAction)

        self.aboutMenu = QMenu('About')
        self.mainMenu.addMenu(self.aboutMenu)

        self.aboutMenu.addAction('About', self.about)

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
        if isWindowsOS():
            self.createShortcutButton = QPushButton('Create Shortcut')
            self.createShortcutButton.setFixedWidth(100)
            self.controlsLayout.addWidget(self.createShortcutButton)
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

        self.appLabel = QLabel('Application')
        self.appCombo = QComboBox()
        self.appCombo.addItems(list(applications.keys()))  # To function
        self.appCombo.currentTextChanged.connect(self.fillVersionCombo)
        self.versionLabel = QLabel('Version')
        self.versionCombo = QComboBox()
        self.fillVersionCombo()
        self.flagsTabTopRightSpacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.flagsTabTopLayout.addWidget(self.appLabel)
        self.flagsTabTopLayout.addWidget(self.appCombo)
        self.flagsTabTopLayout.addWidget(self.versionLabel)
        self.flagsTabTopLayout.addWidget(self.versionCombo)
        self.flagsTabTopLayout.addSpacerItem(self.flagsTabTopRightSpacer)

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
        self.middleButtonsSpacerBottom = QSpacerItem(10, 10, QSizePolicy.Ignored, QSizePolicy.Expanding)
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

        self.fillPresetList()

    def fillVersionCombo(self):
        self.versionCombo.clear()
        self.versionCombo.addItems(sorted(applications[self.appCombo.currentText()], reverse=True))

    def settings(self):
        self.settingsWindow.exec_()

    def about(self):
        raise NotImplementedError

    def fillPresetList(self):
        for preset in loadPresets():
            item = QListWidgetItem(os.path.basename(os.path.splitext(preset)[0]), self.presetList)

    def presetListMenu(self):
        menu = QMenu()
        ACTIONS = {'New preset': 1}
        for a in ACTIONS:
            action = QAction(a)
            menu.addAction()
        menu.exec_(QCursor.pos())

    def launch(self):
        cmd = r'S:\Houdini 16.5.588\bin\houdinifx.exe'
        if os.path.exists(cmd):
            os.system(cmd)

    def createShortcut(self):
        # Windows only
        pass

    def addApplication(self):
        appLink = QFileDialog.getOpenFileName(self, caption='Application', filter='Application (*.exe)')[0]
        if appLink:
            item = QListWidgetItem(appLink, self.allAppsList)
            item.setCheckState(Qt.Checked)
