from typing import Type, List

from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QDialog, QRadioButton, QDoubleSpinBox, QComboBox

from Model.BaseProperty import BaseProperty
from Model.CoolPropInterface import get_available_input_properties, get_other_input_properties
from Model.VarState import VarState, Value, IndValue, Variable, DepValue, State, StateValue, IDGen
from UI.UI_State import Ui_Dialog


class StateWindow(QDialog):
    state_created: Signal = Signal(State)
    state_edited: Signal = Signal()

    def __init__(self, parent, id_gen: IDGen, fluids: List[str], var_states: List[VarState], edit: State = None,
                 restricted_nos: List[int] = None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.idGen = id_gen
        self.edit = edit
        self.restricted_nos = restricted_nos

        self.ups_var_states: List[VarState] = var_states
        self.ups_states: List[State] = [vs for vs in self.ups_var_states if isinstance(vs, State)]
        if self.ups_states:
            no: int = max([s.no for s in self.ups_states]) + 1
            self.ui.spin_stateNo.setValue(no)

        self.ui.cb_input_fluid.currentIndexChanged.connect(self.setup_cb_input_1)

        self.ui.cb_input_1.currentIndexChanged.connect(self.setup_cb_unit_1)
        self.ui.cb_input_1.currentIndexChanged.connect(self.setup_cb_input_2)

        self.ui.cb_input_2.currentIndexChanged.connect(self.setup_cb_unit_2)

        self.ui.cb_input_fluid.addItems(fluids)
        if var_states:
            for vs in var_states:
                self.ui.cb_dep_var_1.addItem(vs.name, vs)
                self.ui.cb_dep_var_2.addItem(vs.name, vs)
        else:
            self.ui.rb_dep1.setEnabled(False)
            self.ui.rb_dep2.setEnabled(False)

        self.state_created.connect(self.parent().new_state_created)
        self.state_created.connect(self.parent().old_state_edited)

        if edit is not None:
            self.setup_edit()

        self.setFixedSize(self.size())

    def setup_edit(self):
        s: State = self.edit
        self.ui.spin_stateNo.setValue(s.no)
        self.setWindowTitle(f"State {s.no}")
        if s.desc:
            self.ui.pte_desc.setPlainText(s.desc)

        self.ui.cb_input_fluid.setCurrentText(s.fluid)
        self.ui.cb_input_1.setCurrentText(s.class_property_1.label)
        self.ui.cb_input_2.setCurrentText(s.class_property_2.label)
        self.ui.cb_unit_1.setCurrentText(s.unit_1)
        self.ui.cb_unit_2.setCurrentText(s.unit_2)

        if isinstance(s.inp_1, IndValue):
            self.ui.dspin_1.setValue(s.inp_1.value)
        else:
            self.ui.rb_dep1.setChecked(True)

            if isinstance(s.inp_1, StateValue):
                self.ui.cb_dep_var_1.setCurrentText(s.inp_1.state.name)
            elif isinstance(s.inp_1, DepValue):
                self.ui.cb_dep_var_1.setCurrentText(s.inp_1.var_ref.name)

        if isinstance(s.inp_2, IndValue):
            self.ui.dspin_2.setValue(s.inp_2.value)
        else:
            self.ui.rb_dep2.setChecked(True)

            if isinstance(s.inp_2, StateValue):
                self.ui.cb_dep_var_2.setCurrentText(s.inp_2.state.name)
            elif isinstance(s.inp_2, DepValue):
                self.ui.cb_dep_var_2.setCurrentText(s.inp_2.var_ref.name)

    @Slot()
    def setup_cb_input_1(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        if fluid == "":
            return

        self.ui.cb_input_1.clear()
        for class_property in get_available_input_properties(fluid):
            self.ui.cb_input_1.addItem(class_property.label, class_property)

    @Slot()
    def setup_cb_input_2(self):
        class_property_1: Type[BaseProperty] = self.ui.cb_input_1.currentData()
        if class_property_1 is None:
            return

        previous_property: Type[BaseProperty] = self.ui.cb_input_2.currentData()
        fluid: str = self.ui.cb_input_fluid.currentText()
        self.ui.cb_input_2.clear()
        other_input_properties: List[Type[BaseProperty]] = get_other_input_properties(fluid, class_property_1)
        for class_property in other_input_properties:
            self.ui.cb_input_2.addItem(class_property.label, class_property)

        if previous_property in other_input_properties:
            self.ui.cb_input_2.setCurrentText(previous_property.label)

    @Slot()
    def setup_cb_unit_1(self):
        class_property: BaseProperty = self.ui.cb_input_1.currentData()
        if class_property is None:
            return
        self.ui.cb_unit_1.clear()
        for unit in class_property.units:
            unit: str
            self.ui.cb_unit_1.addItem(unit)
        self.ui.cb_unit_1.setCurrentText(class_property.get_curr_unit())

    @Slot()
    def setup_cb_unit_2(self):
        class_property: Type[BaseProperty] = self.ui.cb_input_2.currentData()
        if class_property is None:
            return

        self.ui.cb_unit_2.clear()
        for unit in class_property.units:
            unit: str
            self.ui.cb_unit_2.addItem(unit)
        self.ui.cb_unit_2.setCurrentText(class_property.get_curr_unit())

    @Slot()
    def on_buttonBox_accepted(self):
        no: int = self.ui.spin_stateNo.value()
        err_str = self.getNoErr()
        if err_str:
            self.ui.spin_stateNo.setStyleSheet("border: 2px solid red")
            self.ui.spin_stateNo.setFocus()
            self.ui.lb_error.setText(err_str)

            def noRed():
                self.ui.spin_stateNo.setStyleSheet("")
                self.ui.spin_stateNo.valueChanged.disconnect(noRed)

            self.ui.spin_stateNo.valueChanged.connect(noRed)
            return
        desc: str = self.ui.pte_desc.toPlainText()
        class_property_1: Type[BaseProperty] = self.ui.cb_input_1.currentData()
        class_property_2: Type[BaseProperty] = self.ui.cb_input_2.currentData()
        unit_1: str = self.ui.cb_unit_1.currentText()
        unit_2: str = self.ui.cb_unit_2.currentText()
        fluid: str = self.ui.cb_input_fluid.currentText()

        input_1: Value = self.getValue(1)
        input_2: Value = self.getValue(2)

        if self.edit is None:
            st: State = State(no=no, uid=self.idGen.nextID(), fluid=fluid, desc=desc,
                              class_property_1=class_property_1, class_property_2=class_property_2,
                              inp_1=input_1, inp_2=input_2, unit_1=unit_1, unit_2=unit_2)
            self.state_created.emit(st)
        else:
            self.edit.edit(no=no, fluid=fluid, desc=desc,
                           class_property_1=class_property_1, class_property_2=class_property_2,
                           inp_1=input_1, inp_2=input_2, unit_1=unit_1, unit_2=unit_2)
            self.state_edited.emit()

        self.close()

    @Slot()
    def on_buttonBox_rejected(self):
        self.close()

    def getValue(self, input_no: int) -> Value:
        n = input_no - 1
        rb_dep = (self.ui.rb_dep1, self.ui.rb_dep2)
        rb_ind = (self.ui.rb_indep1, self.ui.rb_indep2)
        dspin_ind = (self.ui.dspin_1, self.ui.dspin_2)
        cb_dep = (self.ui.cb_dep_var_1, self.ui.cb_dep_var_2)
        cb_unit = (self.ui.cb_unit_1, self.ui.cb_unit_2)
        cb_cls_props = (self.ui.cb_input_1, self.ui.cb_input_2)

        unit: str = cb_unit[n].currentText()
        rb_i: QRadioButton = rb_ind[n]
        rb_d: QRadioButton = rb_dep[n]
        dspin: QDoubleSpinBox = dspin_ind[n]
        cb: QComboBox = cb_dep[n]
        cb_prop: QComboBox = cb_cls_props[n]

        class Scope:
            value: Value = ...

        if rb_i.isChecked():
            Scope.value = IndValue(value=dspin.value())
        elif rb_d.isChecked():
            v: VarState = cb.currentData()
            if isinstance(v, Variable):
                Scope.value = DepValue(var_ref=v)
            elif isinstance(v, State):
                Scope.value = StateValue(state=v, class_property=cb_prop.currentData(), unit=unit)
            else:
                raise Exception("Unexpected Error")
        else:
            raise Exception("Unexpected")

        return Scope.value

    def getNoErr(self) -> str:
        no: int = self.ui.spin_stateNo.value()

        if self.restricted_nos is not None:
            if no in self.restricted_nos:
                return "State No. is already used"
        else:
            if no in [vs.no for vs in self.ups_states]:
                return "State No. is already used"

        return ""
