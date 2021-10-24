from typing import List

from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QDialog, QCheckBox, QLabel

from Model.CoolPropInterface import Fluids
from UI.Qt_custom import show_error_msg
from UI.UI_FluidsDialog import Ui_Dialog


class FluidsDialog(QDialog):

    def __init__(self, parent, fluids: List[str]):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.fluids_list: List[str] = Fluids.all
        self.curr_fluids: List[str] = fluids
        self.chk_boxes: List[QCheckBox] = []

        for i, fluid in enumerate(self.fluids_list):
            path: str = ":/png/Resources/formula/" + fluid + ".png"
            lb_formula: QLabel = QLabel()
            lb_formula.setPixmap(QPixmap(path))
            chk_box = QCheckBox()
            if fluid in self.curr_fluids:
                chk_box.setChecked(True)
            self.ui.gridLayout.addWidget(chk_box, i, 0)
            self.ui.gridLayout.addWidget(QLabel(fluid), i, 1)
            self.ui.gridLayout.addWidget(lb_formula, i, 2)

            self.chk_boxes.append(chk_box)
            self.setFixedWidth(self.width())

    @Slot()
    def on_buttonBox_accepted(self):
        curr_fluids: List[str] = []
        for i, chk_box in enumerate(self.chk_boxes):
            if chk_box.isChecked():
                curr_fluids.append(self.fluids_list[i])
        if len(curr_fluids) != 0:
            self.curr_fluids.clear()
            self.curr_fluids.extend(curr_fluids)
        else:
            show_error_msg(self, e="Fluid List cannot be empty. No changes were made")
