import sys
import os
import json
import re

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


class ArgumentsWidgetItem(object):
    def __init__(self, name=None, description='', template={}):
        self._name = name
        self._description = description
        self._template = template

    def setName(self, name=None):
        if not name:
            self._name = name

    # def setText(self, text):
    #     self.setName(text)

    def setDescription(self, description=''):
        if not description:
            self._description(description)

    def addFlag(self, description=''):
        pass

    def addInteger(self, description=''):
        pass

    def addFloat(self, description=''):
        pass

    def addString(self, description=''):
        pass

    def addComboBox(self, components={}, description=''):
        pass

    # def setTemplate(self):
    #     pass
    #
    # def addTemplate(self):
    #     pass

    # def loadTemplateFromFile(self, file, name):
    #     pass


class ArgumentsWidget(QW.QWidget):
    def __init__(self, parent=None):
        super(ArgumentsWidget, self).__init__(parent)
        self._elements = {}  # Visual Elements

        self.scrollLayout = QW.QVBoxLayout()
        self.scrollAreaWidget = QW.QWidget()
        self.scrollAreaWidget.setLayout(self.scrollLayout)

        self.scrollArea = QW.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.mainLayout = QW.QVBoxLayout(self)
        self.mainLayout.addWidget(self.scrollArea)

        self.spacerItem = QW.QSpacerItem(20, 40, QW.QSizePolicy.Minimum, QW.QSizePolicy.Expanding)

        # string = r'-geometry #int(Width) #int(Height)+#int(Left)+#int(Top) #string(Haha) #combobox["k":"Kilobytes", "M":"Megabytes"]()'
        # for i in range(100):
        #     self.createElements(string)
        #
        # self.createElements(string)

    def createElements(self, template):
        MinValue = -999999
        MaxValue = +999999
        FixedWidth = 50
        FixedHeight = 25

        variables = re.findall(r'\#.*?\)', template)
        if len(variables) < 1:
            return
        widget = QW.QWidget(self.scrollAreaWidget)
        # widget.setSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Preferred)
        layout = QW.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        label = QW.QCheckBox('Argument name')
        label.setFixedSize(100, FixedHeight)
        layout.addWidget(label)
        for var in variables:
            varType = var[1:4].lower()
            # comboItems = {'k': 'Kilobytes', 'M': 'Megabytes'}
            comboItems = var[var.find('['):var.find(']')+1].replace('[', '{').replace(']', '}')
            if comboItems:
                comboItems = json.loads(comboItems)
                # print(comboItems)
            hint = var[var.find('(')+1:var.find(')')]
            if varType == 'int':
                integer = QW.QSpinBox()
                integer.setFixedSize(FixedWidth, FixedHeight)
                # integer.setValue(0)
                integer.setMinimum(MinValue)
                integer.setMaximum(MaxValue)
                integer.setToolTip(hint)
                layout.addWidget(integer)
            elif varType == 'flo':
                real = QW.QDoubleSpinBox()
                real.setFixedSize(FixedWidth, FixedHeight)
                # real.setValue(0)
                real.setMinimum(MinValue)
                real.setMaximum(MaxValue)
                real.setToolTip(hint)
                layout.addWidget(real)
            elif varType == 'str':
                string = QW.QLineEdit()
                string.setMinimumWidth(60)
                string.setFixedHeight(FixedHeight)
                # string.setText('')
                string.setToolTip(hint)
                layout.addWidget(string)
            elif varType == 'com':
                combo = QW.QComboBox()
                combo.setFixedSize(100, FixedHeight)
                # combo.setCurrentIndex(0)
                for name, hint in comboItems.items():
                    combo.addItem('{} ({})'.format(name, hint), name)
                layout.addWidget(combo)
                combo.setToolTip(hint)
        self.scrollLayout.removeItem(self.spacerItem)
        self.scrollLayout.addWidget(widget)
        self.scrollLayout.addItem(self.spacerItem)

    def addArgument(self, name, description, template):
        pass

    def addItem(self, item: ArgumentsWidgetItem):
        pass

    def clear(self):
        pass

    def loadFromText(self, text):
        pass

    def loadFromFile(self, file):
        with open(file, 'rt') as file:
            self.loadFromText(file.read())


if __name__ == '__main__':
    app = QW.QApplication([])
    window = ArgumentsWidget()
    window.show()
    sys.exit(app.exec_())