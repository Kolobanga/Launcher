import os
import subprocess
import sys

from config import Config
from preset import Preset

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
    if isWindowsOS():
        return os.path.join(os.path.expanduser('~'), 'Documents', 'Launcher')
    else:
        return os.path.join(os.path.expanduser('~'), 'Launcher')


def isWindowsOS():
    return sys.platform.startswith('win')


def isLinuxOS():
    return sys.platform.startswith('linux')


def isMacOS():
    return sys.platform == 'darwin'


def loadConfigs():
    configs = {}
    for directory in rootDir(), homeDir():
        for root, folders, files in os.walk(os.path.join(directory, 'configs')):
            for file in files:
                if file.lower().endswith('.cfg'):
                    config = Config().loadFromFile(os.path.join(root, file))
                    configs[config.name()] = config
    return configs


def loadPresets():
    presets = {}
    for directory in rootDir(), homeDir():
        for root, folders, files in os.walk(os.path.join(directory, 'presets')):
            for file in files:
                if file.lower().endswith('.set'):
                    preset = Preset().loadFromFile(os.path.join(root, file))
                    presets[preset.name()] = preset
    return presets


def launchApplication():
    if isWindowsOS():
        raise NotImplementedError
        # subprocess.call()
    elif isLinuxOS():
        raise NotImplementedError
    elif isMacOS():
        raise NotImplementedError


def createWindowsDesktopShortcut(targetFile, name, icon, comment=None, workDir=None):
    import win32com.client
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(shell.SpecialFolders("Desktop"), name + '.lnk'))
    shortcut.TargetPath = targetFile
    shortcut.IconLocation = icon
    shortcut.WindowStyle = 1
    shortcut.save()


class NewPresetDialog(QDialog):
    def __init__(self, parent=None):
        super(NewPresetDialog, self).__init__(parent)

        # Window
        self.setWindowTitle('New Preset')
        self.setFixedSize(QSize(220, 120))

        QVBoxLayout(self)

        self.presetNameEdit = QLineEdit()
        self.presetNameEdit.setPlaceholderText('Name...')
        self.layout().addWidget(self.presetNameEdit)

        self.configCombo = QComboBox()

        for config in loadConfigs().values():
            self.configCombo.addItem(config.name(), config)
        self.layout().addWidget(self.configCombo)

        self.bottomButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal)
        self.bottomButtons.setCenterButtons(True)
        self.bottomButtons.accepted.connect(self.accept)
        self.bottomButtons.rejected.connect(self.reject)
        self.layout().addWidget(self.bottomButtons)

    def name(self):
        return self.presetNameEdit.text()

    def config(self):
        return self.configCombo.currentData(Qt.UserRole)

    @staticmethod
    def getData(parent=None):
        dialog = NewPresetDialog(parent)
        result = dialog.exec_()
        return dialog.name(), dialog.config(), result == QDialog.Accepted


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window
        self.setWindowTitle('DCC Launcher')
        self.setMinimumSize(QSize(600, 400))
        self.resize(QSize(800, 500))

        # Central Widget
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # Main Menu
        self.mainMenu = QMenuBar()
        self.setMenuBar(self.mainMenu)

        self.quitAction = QAction('Quit', self)
        self.quitAction.triggered.connect(lambda: qApp.exit(0))

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
        self.presetList.itemClicked.connect(self.editPreset)
        for preset in loadPresets().values():
            item = QListWidgetItem(preset.name(), self.presetList)
            item.setData(Qt.UserRole, preset)
        self.presetList.setFixedWidth(130)
        self.middleHorizontalLayout.addWidget(self.presetList)
        self.rightMiddleLayout = QVBoxLayout()
        self.middleHorizontalLayout.addLayout(self.rightMiddleLayout)

        # Right Controls
        self.controlsLayout = QHBoxLayout()

        # New Preset Button
        self.newPresetButton = QPushButton('New Preset')
        self.newPresetButton.setFixedWidth(80)
        self.newPresetButton.clicked.connect(self.newPreset)
        self.controlsLayout.addWidget(self.newPresetButton)

        # Save Preset Button
        self.savePresetButton = QPushButton('Save')
        self.savePresetButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.savePresetButton)

        # Delete Preset Button
        self.deletePresetButton = QPushButton('Delete')
        self.deletePresetButton.clicked.connect(self.deletePreset)
        self.controlsLayout.addWidget(self.deletePresetButton)

        # Spacer
        self.controlsSpacerItem = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.controlsLayout.addSpacerItem(self.controlsSpacerItem)

        # Create Shortcut Button
        if isWindowsOS():
            self.createShortcutButton = QPushButton('Create Shortcut')
            self.createShortcutButton.clicked.connect(self.createShortcut)
            self.createShortcutButton.setFixedWidth(100)
            self.controlsLayout.addWidget(self.createShortcutButton)

        # Launch Button
        self.launchButton = QPushButton('Launch')
        self.launchButton.clicked.connect(self.launchPreset)
        self.launchButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.launchButton)

        self.rightMiddleLayout.addLayout(self.controlsLayout)

        # Tabs
        self.tabs = QTabWidget()
        self.rightMiddleLayout.addWidget(self.tabs)

        # Flags Tab
        self.flagsWidget = ArgumentsWidget()
        self.tabs.addTab(self.flagsWidget, 'Command line Flags')

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

        # All Apps
        self.addAppButton = QPushButton('Add Applications')
        self.addAppButton.clicked.connect(self.addApplication)
        self.allAppsList = QListWidget()
        appsListPath = os.path.join(homeDir(), 'AppsPaths.apps')
        if os.path.exists(appsListPath):
            with open(appsListPath, 'rt') as file:
                for line in file:
                    line = line.rstrip('\n')
                    if os.path.exists(line):
                        QListWidgetItem(line, self.allAppsList)
        self.appTabLeftLayout = QVBoxLayout()
        self.appTabLeftLayout.addWidget(self.addAppButton)
        self.appTabLeftLayout.addWidget(self.allAppsList)
        self.appTabMainLayout.addLayout(self.appTabLeftLayout)

        # Middle Buttons
        self.middleButtonsLayout = QVBoxLayout()
        self.appTabMainLayout.addLayout(self.middleButtonsLayout)
        self.middleButtonsSpacerTop = QSpacerItem(10, 10, QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.middleButtonsLayout.addSpacerItem(self.middleButtonsSpacerTop)
        self.moveAppRight = QPushButton('>>')
        self.moveAppRight.setFixedWidth(25)
        self.middleButtonsLayout.addWidget(self.moveAppRight)
        self.moveAppLeft = QPushButton('<<')
        self.moveAppLeft.setFixedWidth(25)
        self.middleButtonsLayout.addWidget(self.moveAppLeft)
        self.middleButtonsSpacerBottom = QSpacerItem(10, 10, QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.middleButtonsLayout.addSpacerItem(self.middleButtonsSpacerBottom)

        # Added Apps
        self.presetAppsList = QListWidget()
        self.appTabMainLayout.addWidget(self.presetAppsList)
        self.tabs.addTab(self.appTab, 'Applications')

        qApp.configs = loadConfigs()

    def newPreset(self):
        answer = NewPresetDialog.getData(self)
        if answer[2] and answer[0]:  # Accepted and not empty name
            name = answer[0]
            preset = Preset(answer[1])
            preset.setName(name)
            filename = os.path.join(homeDir(), 'presets', name + '.set')
            if os.path.exists(filename):
                dialog = QMessageBox(QMessageBox.Information,
                                     'Confirm File Replace',
                                     'Would you like to replace existing preset?',
                                     QMessageBox.Ok | QMessageBox.Cancel)
                if dialog.exec_() == QMessageBox.Rejected:
                    return
            preset.saveToFile(filename)

            item = QListWidgetItem(name, self.presetList)
            item.setData(Qt.UserRole, preset)

    def deletePreset(self):
        if len(self.presetList.selectedIndexes()) == 0:
            return
        dialog = QMessageBox(QMessageBox.Information,
                             'Confirm File Delete',
                             'Would you like to delete this preset?',
                             QMessageBox.Ok | QMessageBox.Cancel)
        if dialog.exec_() == QMessageBox.Rejected:
            return
        os.remove(self.presetList.currentItem().data(Qt.UserRole).file())
        self.presetList.currentItem().setHidden(True)

    def about(self):
        raise NotImplementedError

    def launchPreset(self):
        cmd = r'S:\Houdini 16.5.588\bin\houdinifx.exe'
        if os.path.exists(cmd):
            subprocess.call(cmd)

    def createShortcut(self):
        """Windows only"""
        createWindowsDesktopShortcut(sys.executable, 'pyme', r'S:\DaVinci Resolve\Resolve.exe')


    def addApplication(self):
        appLink = QFileDialog.getOpenFileName(self, caption='Application', filter='Application (*.exe)')[0]
        if appLink:
            QListWidgetItem(appLink, self.allAppsList)
            # item.setCheckState(Qt.Checked)

    def editPreset(self, item):
        preset = item.data(Qt.UserRole)
        self.flagsWidget.clear()
        self.flagsWidget.createLinesFromConfig(preset.config())

    def saveAppsList(self):
        links = set()
        for index in range(self.allAppsList.count()):
            links.add(self.allAppsList.item(index).text())
        with open(os.path.join(homeDir(), 'AppsPaths.apps'), 'wt') as file:
            for link in links:
                file.write(link + '\n')
