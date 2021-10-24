from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPen, QColor, QValidator, QIcon
from PySide2.QtWidgets import QLineEdit, QSlider, QMessageBox, QStyle
from typing import List

from Model.VarState import Variable

pen = QPen()
pen.setColor(QColor("gray"))


def show_error_msg(parent=None, title: str = "Error", txt: str = "", e: str = None, details: str = None):
    if not txt:
        txt = "An Error Occurred"
    len_txt: int = len(txt)
    width: int = 50
    if len_txt < width:
        txt = txt + " " * (width - len_txt)
    msgBox = QMessageBox(parent)
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(txt + "\t(◕︵◕)\n" + e)
    if details is not None:
        msgBox.setDetailedText(details)

    msgBox.setWindowTitle(title)
    icon: QIcon = msgBox.style().standardIcon(QStyle.SP_MessageBoxCritical)
    msgBox.setWindowIcon(icon)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()


class Cat:
    emo: List[str] = ["(◐ᴥ◐)", "(◑ᴥ◑)"]

    def __init__(self):
        self.flag: int = 0

    def next(self) -> str:
        if self.flag == 0:
            self.flag = 1
            return self.emo[1]
        else:
            self.flag = 0
            return self.emo[0]


class MyLineEdit(QLineEdit):

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.selectAll()


class VarNameValidator(QValidator):
    def validate(self, arg__1: str, arg__2: int) -> QValidator.State:
        if arg__1 == "":
            return QValidator.State.Intermediate
        elif len(arg__1) > 15:
            return QValidator.State.Invalid

        if arg__1.isidentifier():
            return QValidator.State.Acceptable
        else:
            return QValidator.State.Invalid


class KittyTable(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat = Cat()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() > 0:
            return
        painter = QtGui.QPainter(self.viewport())
        painter.save()

        painter.setPen(pen)

        fnt = painter.font()
        fnt.setPointSize(20)
        painter.setFont(fnt)
        painter.drawText(self.viewport().rect(), QtCore.Qt.AlignCenter, self.cat.next())
        painter.restore()


class KittyList(QtWidgets.QListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat = Cat()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() > 0:
            return
        painter = QtGui.QPainter(self.viewport())
        painter.save()

        painter.setPen(pen)

        fnt = painter.font()
        fnt.setPointSize(20)
        painter.setFont(fnt)
        painter.drawText(self.viewport().rect(), QtCore.Qt.AlignCenter, self.cat.next())
        painter.restore()


class DoubleSlider(QSlider):
    doubleValueChanged = Signal(object, float)
    doubleSliderReleased = Signal(object, float)

    def __init__(self, v: Variable, decimals=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.v: Variable = v

        self.setOrientation(Qt.Horizontal)
        self._multi = 10 ** decimals

        self.valueChanged.connect(self.emitDoubleValueChanged)
        self.sliderReleased.connect(self.emitSliderReleased)
        self.refresh()

    def refresh(self):
        v = self.v
        val = v.inp.value
        r1, r2 = v.getRange()
        self.setMinimum(r1)
        self.setMaximum(r2)
        self.setValue(val)
        self.setTickInterval(int((r2 - r1) / 5 * self._multi))
        self.setTickPosition(QSlider.TicksAbove)

    def emitDoubleValueChanged(self):
        value = float(super().value()) / self._multi
        self.doubleValueChanged.emit(self.v, value)

    def emitSliderReleased(self):
        value = float(super().value()) / self._multi
        self.doubleSliderReleased.emit(self.v, value)

    def value(self):
        return float(super().value()) / self._multi

    def setMinimum(self, value):
        return super().setMinimum(value * self._multi)

    def setMaximum(self, value):
        return super().setMaximum(value * self._multi)

    def setSingleStep(self, value):
        return super().setSingleStep(value * self._multi)

    def singleStep(self):
        return float(super().singleStep()) / self._multi

    def setValue(self, value):
        super().setValue(int(value * self._multi))
