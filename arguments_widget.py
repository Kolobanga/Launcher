import json

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


class ArgumentsWidget(QWidget):
    def __init__(self, parent=None):
        super(ArgumentsWidget, self).__init__(parent)
        self.__flagsWidgets = {}  # Visual Elements

        self.scrollAreaWidget = QWidget()
        QVBoxLayout(self.scrollAreaWidget)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.scrollArea)

        self.spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def createLine(self, flagData):
        lineLayout = QHBoxLayout()
        lineLayout.setContentsMargins(0, 0, 0, 0)
        lineLayout.setSpacing(2)

        nameCheckBox = QCheckBox(flagData.get('Name'))
        nameCheckBox.setToolTip(flagData.get('Description'))
        lineLayout.addWidget(nameCheckBox)

        fieldWidgets = {}

        fields = flagData.get('Fields')
        if fields:
            for fieldName, defaultValue in fields.items():
                widget = None
                hint = fieldName.replace('_', ' ')
                if isinstance(defaultValue, int):
                    widget = QSpinBox()
                    widget.setValue(defaultValue)
                    widget.setToolTip(hint)
                elif isinstance(defaultValue, float):
                    widget = QDoubleSpinBox()
                    widget.setValue(defaultValue)
                    widget.setToolTip(hint)
                elif isinstance(defaultValue, bool):
                    widget = QCheckBox()
                    widget.setCheckState(defaultValue)
                    widget.setToolTip(defaultValue)
                elif isinstance(defaultValue, str):
                    widget = QLineEdit(defaultValue)
                    widget.setToolTip(hint)
                elif isinstance(defaultValue, list):
                    widget = QComboBox()
                    for value in defaultValue:
                        widget.addItem(value, value)
                elif isinstance(defaultValue, dict):
                    widget = QComboBox()
                    for description, value in defaultValue.items():
                        widget.addItem(description, value)
                    widget.setToolTip(hint)
                if widget:
                    lineLayout.addWidget(widget)
            fieldWidgets[fieldName] = widget
        self.__flagsWidgets[flagData.get('Name')] = fieldWidgets
        self.scrollAreaWidget.layout().removeItem(self.spacerItem)
        self.scrollAreaWidget.layout().addLayout(lineLayout)
        self.scrollAreaWidget.layout().addItem(self.spacerItem)

    def createLinesFromConfig(self, config):
        for flag in config.flags().values():
            self.createLine(flag)

    def clear(self):
        self.__flagsWidgets.clear()
        clearLayout(self.scrollAreaWidget.layout())


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
        window.createLine(flag)

    k.show()
    app.exec_()
