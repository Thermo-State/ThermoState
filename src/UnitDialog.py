from typing import List

from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QLabel, QComboBox

from Model.CoolPropInterface import list_properties_unit
from UI.UI_UnitDialog import Ui_Dialog


def set_unit(unit: str):
    for class_property in list_properties_unit:
        class_property.set_curr_unit(unit)


def load_custom_units(custom_units: List[str]):
    for i, class_property in enumerate(list_properties_unit):
        class_property.set_curr_unit(custom_units[i])


class UnitDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui: Ui_Dialog = Ui_Dialog()
        self.ui.setupUi(self)

        self.custom_units: List[str] = []
        self.lb_list: List[QLabel] = []
        self.cb_list: List[QComboBox] = []

        for i, class_property in enumerate(list_properties_unit):
            lb: QLabel = QLabel()
            lb.setText(class_property.label)

            cb: QComboBox = QComboBox()
            for unit_i in class_property.units:
                cb.addItem(unit_i)
            cb.setCurrentText(class_property.get_curr_unit())

            self.lb_list.append(lb)
            self.cb_list.append(cb)

            lb.setObjectName("label" + str(i))
            cb.setObjectName("comboBox" + str(i))

            self.ui.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, lb)
            self.ui.formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, cb)

        self.ui.buttonBox.accepted.connect(self.btn_ok)
        self.setFixedSize(self.size())

    def btn_ok(self):
        for i, class_property in enumerate(list_properties_unit):
            unit: str = self.cb_list[i].currentText()
            class_property.set_curr_unit(unit)
            self.custom_units.append(unit)
