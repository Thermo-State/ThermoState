from typing import Optional, Type, Union, List

from PySide2.QtCore import Slot, Signal, QPoint
from PySide2.QtWidgets import QDialog

from ExprDialog import ExprDialog
from Model import CoolPropInterface
from Model.BaseProperty import BaseProperty
from Model.VarState import VarState, Variable, IndValue, Value, ExprValue, State, StateValue, MATH_NS, IDGen
from Model.viewModels2 import VarInTableModel
from UI.Qt_custom import VarNameValidator
from UI.UI_Variable import Ui_Dialog


class VarWindow(QDialog):
    var_created: Signal = Signal(Variable)
    var_edited: Signal = Signal(Variable)

    def __init__(self, parent, id_gen: IDGen, var_states: List[VarState], edit: Variable = None,
                 pos: QPoint = None, is_inner: bool = False, restricted_names: List[str] = None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.ln_name.setValidator(VarNameValidator())

        self.idGen = id_gen
        self.edit = edit
        self.restricted_names = restricted_names

        if pos is not None:
            self.move(pos)

        self.ups_var_states: List[VarState] = var_states
        self.ups_vars: List[Variable] = []
        self.ups_states: List[State] = []
        self.inner_vars: List[Variable] = []

        self.expr: List[Union[str, Variable]] = []
        self.expr_dis_str: str = ""

        for vs in self.ups_var_states:
            if isinstance(vs, Variable):
                self.ups_vars.append(vs)
            elif isinstance(vs, State):
                self.ups_states.append(vs)

        self.model_vars_inner: VarInTableModel = VarInTableModel(data=self.inner_vars)
        self.ui.tbv_inner.setModel(self.model_vars_inner)

        self.var_created.connect(self.parent().new_var_created)
        self.var_edited.connect(self.parent().old_var_edited)

        if self.ups_states:
            self.ui.cb_property.currentIndexChanged.connect(self.setup_cb_unit)
            for s in self.ups_states:
                self.ui.cb_state.addItem(s.name, s)
            for cls_prop in CoolPropInterface.list_props_for_var:
                self.ui.cb_property.addItem(cls_prop.label, cls_prop)
        else:
            self.ui.rb_expr.setChecked(True)
            self.ui.rb_state.setEnabled(False)

        if is_inner:
            self.ui.wgt_rng.setEnabled(False)
        self.ui.tbv_inner.setHidden(True)

        if edit is not None:
            self.setup_edit()
        self.setFixedSize(self.size())

    def setup_edit(self):
        v: Variable = self.edit
        self.ui.ln_name.setText(v.name)
        self.setWindowTitle(f"Variable: {v.name}")

        if v.desc:
            self.ui.pte_desc.setPlainText(v.desc)

        self.ui.chb_range.setEnabled(False)

        if isinstance(v.inp, IndValue):
            self.ui.dspin_value.setValue(v.inp.value)
            if v.inp.value_range is not None:
                r1, r2 = v.inp.value_range
                self.ui.chb_range.setChecked(True)
                self.ui.dspin_r1.setValue(r1)
                self.ui.dspin_r2.setValue(r2)

                self.ui.rb_dep.setEnabled(False)
            else:
                self.ui.lb_rng_details.setEnabled(False)

        else:
            self.ui.rb_dep.setChecked(True)

            if isinstance(v.inp, StateValue):
                self.ui.rb_state.setChecked(True)
                self.ui.cb_state.setCurrentText(v.inp.state.name)
                self.ui.cb_property.setCurrentText(v.inp.class_property.label)
                self.ui.cb_unit.setCurrentText(v.inp.unit)
            elif isinstance(v.inp, ExprValue):
                self.ui.rb_expr.setChecked(True)
                if v.inp.inner_vars:
                    self.inner_vars = v.inp.inner_vars
                    self.ui.tbv_inner.setHidden(False)
                    self.model_vars_inner.changeData(self.inner_vars)
                self.expr = v.inp.expr
                self.expr_dis_str = v.inp.definition
                self.ui.lb_expr.setText(self.expr_dis_str)

    @Slot()
    def on_rb_indep_toggled(self):
        self.ui.stwgt_input.setCurrentIndex(0)

    @Slot()
    def on_rb_dep_toggled(self):
        self.ui.stwgt_input.setCurrentIndex(1)

    @Slot()
    def on_chb_range_toggled(self):
        if self.ui.chb_range.isChecked():
            self.ui.wgt_range.setEnabled(True)
        else:
            self.ui.wgt_range.setEnabled(False)

    @Slot()
    def setup_cb_unit(self):
        """ on cb_property currentIndexChanged """
        class_property: BaseProperty = self.ui.cb_property.currentData()
        if class_property is None:
            return
        self.ui.cb_unit.clear()
        for unit in class_property.units:
            unit: str
            self.ui.cb_unit.addItem(unit)
        self.ui.cb_unit.setCurrentText(class_property.get_curr_unit())

    @Slot()
    def on_btn_add_inner_clicked(self):
        pos: QPoint = self.pos()
        pos.setX(pos.x() + 20)
        pos.setY(pos.y() + 20)
        vw: VarWindow = VarWindow(self, id_gen=self.idGen, var_states=self.ups_var_states + self.inner_vars,
                                  pos=pos, is_inner=True)
        vw.exec_()

    @Slot()
    def on_buttonBox_accepted(self):
        name: str = self.ui.ln_name.text()
        err_str = self.getNameErr()
        if err_str:
            self.ui.ln_name.setStyleSheet("border: 2px solid red")
            self.ui.ln_name.setFocus()
            self.ui.lb_error.setText(err_str)

            def noRed():
                self.ui.ln_name.setStyleSheet("")
                self.ui.ln_name.textChanged.disconnect(noRed)
            self.ui.ln_name.textChanged.connect(noRed)

            return
        desc: str = self.ui.pte_desc.toPlainText()

        class Scope:
            value: Value = ...

        if self.ui.rb_indep.isChecked():
            val: float = self.ui.dspin_value.value()
            rng: Optional[tuple] = None

            if self.ui.chb_range.isChecked():
                rng = (self.ui.dspin_r1.value(), self.ui.dspin_r2.value())
                if not rng[0] <= val <= rng[1]:
                    self.ui.lb_error.setText("Range must include entered value")
                    return

            Scope.value = IndValue(value=val, value_range=rng)
        elif self.ui.rb_dep.isChecked():
            if self.ui.rb_state.isChecked():
                state: State = self.ui.cb_state.currentData()
                class_property: Type[BaseProperty] = self.ui.cb_property.currentData()
                unit: str = self.ui.cb_unit.currentText()
                Scope.value = StateValue(state=state, class_property=class_property, unit=unit)
            elif self.ui.rb_expr.isChecked():
                if self.expr:
                    Scope.value = ExprValue(expr=self.expr, inner_vars=self.inner_vars)
                else:
                    self.ui.lb_error.setText("Enter Expression")
                    return

            else:
                return
        else:
            return

        if self.edit is None:
            v = Variable(name=name, uid=self.idGen.nextID(), inp=Scope.value, desc=desc)
            self.var_created.emit(v)
        else:
            self.edit.edit(name=name, inp=Scope.value, desc=desc)
            self.var_edited.emit(self.edit)
        self.close()

    @Slot()
    def on_buttonBox_rejected(self):
        self.close()

    @Slot()
    def on_tbv_inner_doubleClicked(self):
        row: int = self.ui.tbv_inner.currentIndex().row()
        if row == -1:
            return
        restricted_names = [v.name for v in self.inner_vars]
        restricted_names.pop(row)
        restricted_names.extend([v.name for v in self.ups_vars])
        vw = VarWindow(parent=self, id_gen=self.idGen, var_states=self.ups_var_states, edit=self.inner_vars[row],
                       restricted_names=restricted_names)
        vw.exec_()

    @Slot(Variable)
    def new_var_created(self, v: Variable):
        self.inner_vars.append(v)
        self.ui.tbv_inner.setHidden(False)
        self.model_vars_inner.refresh()

    @Slot(list, str)
    def expr_received(self, expr: List[str], expr_dis_str: str):
        self.expr = expr
        self.expr_dis_str = expr_dis_str
        self.ui.lb_expr.setText(expr_dis_str)

    @Slot()
    def on_btn_expr_edit_clicked(self):
        ed: ExprDialog = ExprDialog(self, self.expr, self.ups_vars + self.inner_vars)
        ed.expr_created.connect(self.expr_received)
        ed.exec()

    @Slot(Variable)
    def old_var_edited(self, v: Variable): # noqa
        self.model_vars_inner.refresh()

    def getNameErr(self) -> str:
        name: str = self.ui.ln_name.text()
        if name == "":
            return "Name is Required"
        if self.restricted_names is not None:
            if name in self.restricted_names:
                return "This name is already used"
        else:
            if name in [v.name for v in self.ups_vars]:
                return "This name is already used"
        if not name.isidentifier():
            return "Not Valid Identifier. Identifier is made with a combination of lowercase or uppercase " \
                          "letters, digits or an underscore and cannot start with a digit nor contain any whitespace"
        if name in MATH_NS:
            return "This name conflicts with a math function. Choose other name"

        return ""
