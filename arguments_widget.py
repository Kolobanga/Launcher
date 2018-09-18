import json
import re

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


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
        raise NotImplementedError

    def addInteger(self, description=''):
        raise NotImplementedError

    def addFloat(self, description=''):
        raise NotImplementedError

    def addString(self, description=''):
        raise NotImplementedError

    def addComboBox(self, components={}, description=''):
        raise NotImplementedError

    # def setTemplate(self):
    #     pass
    #
    # def addTemplate(self):
    #     pass

    # def loadTemplateFromFile(self, file, name):
    #     pass


class ArgumentsWidget(QWidget):
    def __init__(self, parent=None):
        super(ArgumentsWidget, self).__init__(parent)
        self._elements = {}  # Visual Elements

        self.scrollAreaWidget = QWidget()
        QVBoxLayout(self.scrollAreaWidget)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.scrollArea)

        self.spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def createLine(self, template, name, description=''):
        MinValue = -999999
        MaxValue = +999999
        FixedWidth = 50
        FixedHeight = 25

        variables = re.findall(r'\#.*?\)', template)
        # if len(variables) < 1:
        #     return
        widget = QWidget(self.scrollAreaWidget)
        widget.setToolTip(description)
        # widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        lineLayout = QHBoxLayout(widget)
        lineLayout.setContentsMargins(0, 0, 0, 0)
        lineLayout.setSpacing(2)
        label = QCheckBox(name)
        label.setFixedHeight(FixedHeight)
        lineLayout.addWidget(label)
        for var in variables:
            varType = var[1:4].lower()
            comboItems = var[var.find('['):var.find(']') + 1].replace('[', '{').replace(']', '}')
            if comboItems:
                comboItems = json.loads(comboItems.replace("'", '"'))
            tip = var[var.find('(') + 1:var.find(')')]
            if varType == 'int':
                integer = QSpinBox()
                integer.setFixedSize(FixedWidth, FixedHeight)
                # integer.setValue(0)
                integer.setMinimum(MinValue)
                integer.setMaximum(MaxValue)
                integer.setToolTip(tip)
                lineLayout.addWidget(integer)
            elif varType == 'flo':
                real = QDoubleSpinBox()
                real.setFixedSize(FixedWidth, FixedHeight)
                # real.setValue(0)
                real.setMinimum(MinValue)
                real.setMaximum(MaxValue)
                real.setToolTip(tip)
                lineLayout.addWidget(real)
            elif varType == 'str':
                string = QLineEdit()
                string.setMinimumWidth(60)
                string.setFixedHeight(FixedHeight)
                # string.setText('')
                string.setToolTip(tip)
                lineLayout.addWidget(string)
            elif varType == 'com':
                combo = QComboBox()
                combo.setFixedHeight(FixedHeight)
                combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
                # combo.setCurrentIndex(0)
                for name, hint in comboItems.items():
                    combo.addItem('{} ({})'.format(name, hint), name)
                lineLayout.addWidget(combo)
                combo.setToolTip(tip)
        rightSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Ignored)
        lineLayout.addSpacerItem(rightSpacer)
        self.scrollAreaWidget.layout().removeItem(self.spacerItem)
        self.scrollAreaWidget.layout().addWidget(widget)
        self.scrollAreaWidget.layout().addItem(self.spacerItem)

    def createLinesFromConfig(self, config):
        for flag in config.flags().values():
            self.createLine(flag.get('Template'), flag.get('Name'), flag.get('Description'))

    def addArgument(self, name, description, template):
        raise NotImplementedError

    def addItem(self, item: ArgumentsWidgetItem):
        raise NotImplementedError

    def clear(self):
        clearLayout(self.scrollAreaWidget.layout())

    def loadFromText(self, text):
        raise NotImplementedError

    def loadFromFile(self, file):
        with open(file, 'rt') as file:
            self.loadFromText(file.read())


class FlagsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


if __name__ == '__main__':
    app = QApplication([])
    k = QTabWidget()
    QVBoxLayout(k)
    window = ArgumentsWidget()
    k.addTab(window, 'Command line Flags')

    # string = r'-geometry #int(Width) #int(Height)+#int(Left)+#int(Top) #string(Haha) #combobox["k":"Kilobytes", "M":"Megabytes"]()'
    with open(r'./configs/Houdini_16.0-16.5.cfg', 'rt') as file:
        data = json.load(file)
    for flag in data['Flags']:
        window.createLine(flag['Template'], flag['Name'], flag['Description'])

    k.show()
    app.exec_()
