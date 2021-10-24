from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QDialog, QStyle, QHeaderView

import UI.formula_rc  # noqa
from Model.CoolPropInterface import get_general_property_objects
from Model.ViewModels import InTableModel
from UI.UI_FluidInfo import Ui_Dialog


class FluidInfoDialog(QDialog):
    def __init__(self, parent, fluid: str):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.lb_name.setText(fluid)
        path: str = ":/png/Resources/formula/" + fluid + ".png"
        self.ui.lb_formula.setPixmap(QPixmap(path))
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        self.ui.tbv_info.setModel(InTableModel(get_general_property_objects(fluid)))
        self.ui.tbv_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setFixedSize(self.size())
