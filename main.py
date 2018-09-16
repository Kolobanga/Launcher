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

from launcher import MainWindow, homeDir, rootDir


def checkHome():
    homePath = homeDir()
    if not os.path.exists(homePath):
        os.mkdir(homePath)
    configsPath = os.path.join(homePath, 'configs')
    if not os.path.exists(configsPath):
        os.mkdir(configsPath)
    presetsPath = os.path.join(homePath, 'presets')
    if not os.path.exists(presetsPath):
        os.mkdir(presetsPath)


if __name__ == '__main__':
    def my_excepthook(type, value, tback):
        sys.__excepthook__(type, value, tback)


    sys.excepthook = my_excepthook
    checkHome()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    exitCode = app.exec_()
    sys.exit(exit())
