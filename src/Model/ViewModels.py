from typing import Any, List

from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex

from .BaseProperty import BaseProperty, InvalidProperty
from .PureSubstances import PureState


class OutTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data: List[BaseProperty] = []
        self.properties: List[BaseProperty] = data
        self.columnLabels: List[str] = ["value", "unit"]

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        property_obj: BaseProperty = self.properties[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return property_obj.in_curr_unit_str()
            if index.column() == 1:
                return property_obj.get_curr_unit()
        if role == Qt.ToolTipRole:
            if index.column() == 0:
                if type(property_obj) == InvalidProperty:
                    property_obj: InvalidProperty
                    return property_obj.error_info()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.properties)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if len(self.properties) != 0:
            return 2
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        property_obj: BaseProperty = self.properties[section]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnLabels[section]
            if orientation == Qt.Vertical:
                return property_obj.symbol
        if role == Qt.ToolTipRole:
            if orientation == Qt.Vertical:
                return property_obj.label

    def changeData(self, data: List[BaseProperty]):
        self.properties = data
        self.layoutChanged.emit()

    def empty(self):
        self.changeData([])

    def refresh(self):
        self.layoutChanged.emit()


class InTableModel(OutTableModel):
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        property_obj: BaseProperty = self.properties[section]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnLabels[section]
            if orientation == Qt.Vertical:
                return property_obj.label


class HistoryTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data: List[PureState] = []
        self.states: List[PureState] = data
        self.columnLabels: List[str] = []

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        property_obj: BaseProperty = self.states[index.row()].get_state_property(index.column())
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
            return self.states[0].get_state_property_count()
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if len(self.states) != 0:
                    prop: BaseProperty = self.states[0].get_state_property(section)
                    return prop.symbol + "\n" + prop.get_curr_unit()
            if orientation == Qt.Vertical:
                if self.states:
                    return self.states[section].no
        if role == Qt.ToolTipRole:
            if orientation == Qt.Horizontal:
                return self.states[0].get_state_property(section).label

    def changeData(self, data: List[PureState]):
        self.states = data
        self.layoutChanged.emit()

    def refresh(self):
        self.layoutChanged.emit()

    def get_property(self, index: QModelIndex):
        return self.states[index.row()].get_state_property(index.column())
