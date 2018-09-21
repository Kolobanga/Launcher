try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *


class CheckBox(QCheckBox):
    def __init__(self):
        super(CheckBox, self).__init__()

    def value(self):
        return self.isChecked()


class LineEdit(QLineEdit):
    def __init__(self):
        super(LineEdit, self).__init__()

    def value(self):
        return self.text()


class ComboBox(QComboBox):
    def __init__(self):
        super(ComboBox, self)

    def value(self):
        return self.currentData(Qt.UserRole)

