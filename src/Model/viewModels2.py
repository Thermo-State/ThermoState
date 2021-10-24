from typing import Any, List, Dict

from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, QAbstractListModel
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

from Model.BaseProperty import BaseProperty, InvalidProperty
from UI.Qt_custom import DoubleSlider
from .VarState import VarState, Variable, State, Flow


class FlowTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data: List[VarState] = []
        self.var_states = data
        self.columnLabels: List[str] = ["Name", "Definition"]

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        var_state: VarState = self.var_states[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return var_state.name
            if index.column() == 1:
                return var_state.definition
        if role == Qt.ToolTipRole:
            if index.column() == 0:
                return var_state.desc

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.var_states)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if len(self.var_states) != 0:
            return 2
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnLabels[section]

    def changeData(self, data: List[VarState]):
        self.var_states = data
        self.layoutChanged.emit()

    def empty(self):
        self.changeData([])

    def refresh(self):
        self.layoutChanged.emit()


class VarTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data: List[VarState] = []
        self.var_states = data
        self.vars: List[Variable] = []
        for vs in self.var_states:
            if vs == type(Variable):
                self.vars.append(vs)
        self.columnLabels: List[str] = ["Name", "Value"]

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        v: Variable = self.vars[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return v.name
            if index.column() == 1:
                return "{:.5g}".format(v.value)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.vars)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if len(self.vars) != 0:
            return 2
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnLabels[section]

    def changeData(self, data: List[VarState]):
        self.var_states = data
        self.refresh()

    def empty(self):
        self.changeData([])

    def refresh(self):
        self.vars.clear()
        for vs in self.var_states:
            if isinstance(vs, Variable):
                self.vars.append(vs)
        self.layoutChanged.emit()


class VarInTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data: List[Variable] = []
        self.vars = data
        self.columnLabels: List[str] = ["Name", "Definition"]

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        v: Variable = self.vars[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return v.name
            if index.column() == 1:
                return v.definition

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.vars)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if len(self.vars) != 0:
            return 2
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnLabels[section]

    def changeData(self, data: List[VarState]):
        self.vars = data
        self.layoutChanged.emit()

    def empty(self):
        self.changeData([])

    def refresh(self):
        self.layoutChanged.emit()


class StateTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data: List[VarState] = []
        self.var_states = data
        self.states: List[State] = []
        for vs in self.var_states:
            if vs == type(State):
                self.states.append(vs)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        property_obj: BaseProperty = self.states[index.row()].value.get_state_property(index.column())
        if role == Qt.DisplayRole:
            return property_obj.in_curr_unit_str()
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.ToolTipRole:
            if type(property_obj) == InvalidProperty:
                property_obj: InvalidProperty
                return property_obj.error_info()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.states)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if len(self.states) != 0:
            return self.states[0].value.get_state_property_count()
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if len(self.states) != 0:
                    prop: BaseProperty = self.states[0].value.get_state_property(section)
                    return prop.symbol + "\n" + prop.get_curr_unit()
            if orientation == Qt.Vertical:
                return self.states[section].no

    def changeData(self, data: List[VarState]):
        self.var_states = data
        self.refresh()

    def empty(self):
        self.changeData([])

    def refresh(self):
        self.states.clear()
        for vs in self.var_states:
            if isinstance(vs, State):
                self.states.append(vs)
        self.layoutChanged.emit()


class SliderTableManager:
    nm: int = 0
    sl: int = 1
    vl: int = 2

    def __init__(self, parent, tbw: QTableWidget, data: List[Variable] = None):
        self.tbw = tbw
        if data is None:
            data: List[Variable] = []
        self.ranged_vars: List[Variable] = data
        self.parent = parent

        row: int = len(self.ranged_vars)
        tbw.setRowCount(row)
        tbw.setColumnCount(3)

        self.map: Dict[int, int] = {}
        for i in range(row):
            self.__addNew(i)

    def newAddedLast(self):
        self.tbw.setRowCount(self.tbw.rowCount() + 1)
        self.__addNew(len(self.ranged_vars) - 1)

    def __addNew(self, i: int):
        v: Variable = self.ranged_vars[i]

        slider: DoubleSlider = DoubleSlider(v)
        slider.doubleValueChanged.connect(self.valueChanged)
        slider.doubleSliderReleased.connect(self.sliderReleased)

        self.__addRow(i, v, slider)

    def valueChanged(self, v: Variable, value: float):
        i: int = self.map[v.uid]
        self.tbw.item(i, self.vl).setText("{:.5g}".format(value))

    def sliderReleased(self, v: Variable, value: float):
        v.inp.value = value
        if self.parent.ui.chb_auto_calc.isChecked():
            self.parent.on_btn_calc_clicked()

    def __addRow(self, i: int, v: Variable, slider: DoubleSlider):
        item = QTableWidgetItem()
        item.setText(v.name)
        item.setToolTip(v.desc)
        item.setTextAlignment(Qt.AlignCenter)
        self.tbw.setItem(i, self.nm, item)

        self.tbw.setCellWidget(i, self.sl, slider)

        item = QTableWidgetItem()
        item.setText("{:.5g}".format(v.inp.value))
        item.setTextAlignment(Qt.AlignCenter)
        self.tbw.setItem(i, self.vl, item)

        self.map[v.uid] = i

    def remap(self):
        self.map.clear()
        for i in range(self.tbw.rowCount()):
            slider: DoubleSlider = self.tbw.cellWidget(i, self.sl)
            self.map[slider.v.uid] = i

    def refresh_at(self, v: Variable):
        i: int = self.map[v.uid]
        slider: DoubleSlider = self.tbw.cellWidget(i, self.sl)
        slider.refresh()
        self.tbw.item(i, self.vl).setText("{:.5g}".format(v.inp.value))
        self.tbw.item(i, self.nm).setText(v.name)
        self.tbw.item(i, self.nm).setToolTip(v.desc)

    def deleteRow(self, row: int):
        self.tbw.removeRow(row)
        self.remap()


class FlowListModel(QAbstractListModel):
    def __init__(self, data: List[Flow] = None):
        super().__init__()
        if data is None:
            data: List[Flow] = []
        self.flows = data
        self.columnLabels: str = "Flow Name"

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        flow: Flow = self.flows[index.row()]
        if role == Qt.DisplayRole:
            return flow.name
        if role == Qt.ToolTipRole:
            return flow.desc

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.flows)

    def changeData(self, data: List[Flow]):
        self.flows = data
        self.layoutChanged.emit()

    def empty(self):
        self.changeData([])

    def refresh(self):
        self.layoutChanged.emit()
