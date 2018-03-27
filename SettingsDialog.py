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

from launcher import getRootDir

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.setWindowTitle('Settings')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = SettingsDialog()
    mainWindow.show()
    sys.exit(app.exec_())
