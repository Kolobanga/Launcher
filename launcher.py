import sys
import os
import json

try:
    from PyQt5 import QtWidgets as QW
    from PyQt5 import QtCore as QC
    from PyQt5 import QtGui as QG
    from PyQt5.Qt import Qt as QT
except ImportError:
    from PySide2 import QtWidgets as QW
    from PySide2 import QtCore as QC
    from PySide2 import QtGui as QG
    from PySide2.QtCore import Qt as QT

from ArgumentsWidget import *


class Preset(object):
    # Applications
    Custom = 0
    Houdini = 1
    # Maya = 2
    # Max = 3  # 3D Studio Max
    Cinema4D = 4
    # Nuke = 5

    def __init__(self, file):
        with open(file) as f:
            json.load(f.read())

def scanPresetsFolder(presetsFolder='./presets'):
    presets = []
    for file in os.listdir(presetsFolder):
        if file.endswith('.set'):
            presets.append(os.path.join('./presets/', file))
    # presets = [f for f in os.listdir(presetsFolder) if f.endswith('.set')]
    return presets


def createNewPreset():
    pass

def launchApplication():
    pass

class MainWindow(QW.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('DCC Launcher')
        self.setMinimumSize(QC.QSize(600, 400))
        self.resize(QC.QSize(800, 500))

        # Central Widget
        self.centralwidget = QW.QWidget()
        self.setCentralWidget(self.centralwidget)

        # Layouts
        self.verticalLayout = QW.QVBoxLayout(self.centralwidget)
        # self.topHorizontalLayout = QW.QHBoxLayout()
        # self.verticalLayout.addLayout(self.topHorizontalLayout)
        self.middleHorizontalLayout = QW.QHBoxLayout()
        self.verticalLayout.addLayout(self.middleHorizontalLayout)
        # Presets Widget
        self.presetList = QW.QListWidget()
        self.presetList.setFixedWidth(130)
        self.middleHorizontalLayout.addWidget(self.presetList)
        self.rightMiddleLayout = QW.QVBoxLayout()
        self.middleHorizontalLayout.addLayout(self.rightMiddleLayout)


        # Right Controls
        self.controlsLayout = QW.QHBoxLayout()
        self.launchButton = QW.QPushButton('Launch')
        self.launchButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.launchButton)
        self.createLinkButton = QW.QPushButton('Create Link')
        self.createLinkButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.createLinkButton)
        self.newPresetButton = QW.QPushButton('New Preset')
        self.newPresetButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.newPresetButton)
        self.saveButton = QW.QPushButton('Save Preset')
        self.saveButton.setFixedWidth(80)
        self.controlsLayout.addWidget(self.saveButton)
        self.controlsSpacerItem = QW.QSpacerItem(20, 20, QW.QSizePolicy.Expanding, QW.QSizePolicy.Ignored)
        self.controlsLayout.addItem(self.controlsSpacerItem)
        self.rightMiddleLayout.addLayout(self.controlsLayout)

        # self.flagsWidget = QW.QWidget(self.centralwidget)
        # self.middleHorizontalLayout.addWidget(self.flagsWidget)

        # self.args = ArgumentsWidget()
        # self.middleHorizontalLayout.addWidget(self.args)

        # houdini16_5 = {'AppName': 'Houdini',
        #           'AppVersion': '16.5',
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

    def fillPresetList(self):
        for preset in scanPresetsFolder():
            item = QW.QListWidgetItem(preset)
            self.presetList.addItem(item)

    def presetListMenu(self):
        menu = QW.QMenu()
        ACTIONS = {'New preset':1}
        for a in ACTIONS:
            action = QW.QAction(a)
            menu.addAction()
        menu.exec_(QG.QCursor.pos())

if __name__ == '__main__':
    app = QW.QApplication(sys.argv)
    mainWindow = MainWindow()

    # Style
    # with open('style.qss', 'rt') as style:
    #     app.setStyleSheet(style.read())

    mainWindow.show()
    sys.exit(app.exec_())
