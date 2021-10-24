import traceback
from typing import Optional, List, Set

from PySide2.QtCore import Slot, Signal
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow, QHeaderView, QAction

from FluidsDialog import FluidsDialog
from Model.VarState import VarState, Variable, State, whichDependsOnIt, Flow, IDGen
from Model.viewModels2 import FlowTableModel, VarTableModel, StateTableModel, SliderTableManager
from StateWindow import StateWindow
from UI.UI_FlowWindow import Ui_MainWindow
from UI.Qt_custom import show_error_msg
from VarWindow import VarWindow


class FlowWindow(QMainWindow):
    flow_created: Signal = Signal(Flow)
    flow_edited: Signal = Signal()
    window_closed: Signal = Signal(QMainWindow)

    def __init__(self, parent, edit: Flow = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.edit: Flow = edit
        if edit is not None:
            self.idGen: IDGen = IDGen(init=edit.getLastID())
            self.fluids = edit.fluids
            self.var_states = edit.var_states
            self.ranged_vars = edit.ranged_vars

            self.ui.ln_name.setText(self.edit.name)
            self.setWindowTitle(f"Flow: {self.edit.name}")
            self.ui.pte_desc.setPlainText(self.edit.desc)

        else:
            self.idGen: IDGen = IDGen()
            self.fluids: List[str] = ["Air", "Water"]
            self.var_states: List[VarState] = []
            self.ranged_vars: List[Variable] = []

        self.setup_table_stretch()

        self.model_flow: FlowTableModel = FlowTableModel(data=self.var_states)
        self.model_vars: VarTableModel = VarTableModel(data=self.var_states)
        self.model_states: StateTableModel = StateTableModel(data=self.var_states)
        self.manager_slider: SliderTableManager = SliderTableManager(self, self.ui.tb_slider, self.ranged_vars)
        self.ui.tbv_flow.setModel(self.model_flow)
        self.ui.tbv_vars.setModel(self.model_vars)
        self.ui.tbv_states.setModel(self.model_states)

        self.setup_actions()
        self.setupFluidsLabel()

    @Slot()
    def on_btn_edit_fluids_clicked(self):
        fd: FluidsDialog = FluidsDialog(self, fluids=self.fluids)
        if fd.exec_():
            conflicts: Set[str] = set()
            for vs in self.var_states:
                if isinstance(vs, State):
                    if vs.fluid not in self.fluids:
                        conflicts.add(vs.fluid)
            if conflicts:
                show_error_msg(txt="{} will be re-added".format(", ".join(conflicts)),
                               e="Found usage of fluid{}"
                                 " in State definition.".format("s" if len(conflicts) > 1 else ""))
                self.fluids.extend(conflicts)

            self.setupFluidsLabel()

    @Slot()
    def on_btn_new_state_clicked(self):
        ns = self.var_states + self.ranged_vars
        sw = StateWindow(parent=self, id_gen=self.idGen, fluids=self.fluids, var_states=ns)
        sw.exec_()

    @Slot()
    def on_btn_new_var_clicked(self):
        ns = self.var_states + self.ranged_vars
        vw = VarWindow(parent=self, id_gen=self.idGen, var_states=ns)
        vw.exec_()

    @Slot()
    def on_btn_calc_clicked(self):
        class Problem:
            vs: Optional[VarState] = None

        try:
            for v in self.ranged_vars:
                v.calculate()
            for vs in self.var_states:
                Problem.vs = vs
                vs.calculate()
        except Exception as e_calc:
            tb_calc: str = traceback.format_exc()
            show_error_msg(parent=self, txt="An Error occurred while calculating " + Problem.vs.name,
                           e=str(e_calc), details=tb_calc)
            return
        self.model_vars.refresh()
        self.model_states.refresh()

    @Slot()
    def on_tbv_flow_doubleClicked(self):
        self.fun_flow_edit()

    @Slot()
    def on_tb_slider_doubleClicked(self):
        self.fun_slider_edit()

    def setup_actions(self):
        editAct_slider = QAction("Edit", self.ui.tb_slider)
        editAct_slider.triggered.connect(self.fun_slider_edit)

        editAct_flow = QAction("Edit", self.ui.tbv_flow)
        editAct_flow.triggered.connect(self.fun_flow_edit)

        dltAct_slider = QAction("Delete", self.ui.tb_slider)
        dltAct_slider.triggered.connect(self.fun_slider_dlt)

        dltAct_flow = QAction("Delete", self.ui.tbv_flow)
        dltAct_flow.triggered.connect(self.fun_flow_dlt)

        self.ui.tbv_flow.addAction(editAct_flow)
        self.ui.tbv_flow.addAction(dltAct_flow)

        self.ui.tb_slider.addAction(editAct_slider)
        self.ui.tb_slider.addAction(dltAct_slider)

    @Slot()
    def fun_flow_edit(self):
        row: int = self.ui.tbv_flow.currentIndex().row()
        if row == -1:
            return
        ns = self.var_states[:row] + self.ranged_vars
        vs = self.var_states[row]
        if isinstance(vs, Variable):
            restricted_names = [vs.name for vs in self.var_states if isinstance(vs, Variable)]
            restricted_names.remove(vs.name)
            restricted_names.extend([ranged_var.name for ranged_var in self.ranged_vars])
            vw = VarWindow(parent=self, id_gen=self.idGen, var_states=ns, edit=vs,
                           restricted_names=restricted_names)
            vw.exec_()
        elif isinstance(vs, State):
            restricted_no = [vs.no for vs in self.var_states if isinstance(vs, State)]
            restricted_no.remove(vs.no)
            sw = StateWindow(parent=self, id_gen=self.idGen, fluids=self.fluids, var_states=ns, edit=vs,
                             restricted_nos=restricted_no)
            sw.exec_()

    @Slot()
    def fun_slider_edit(self):
        row: int = self.ui.tb_slider.currentIndex().row()
        if row == -1:
            return
        v = self.ranged_vars[row]
        restricted_names = [ranged_var.name for ranged_var in self.ranged_vars]
        restricted_names.pop(row)
        restricted_names.extend([vs.name for vs in self.var_states if isinstance(vs, Variable)])
        vw = VarWindow(parent=self, id_gen=self.idGen, var_states=[], edit=v, restricted_names=restricted_names)
        vw.exec_()

    @Slot()
    def fun_flow_dlt(self):
        row: int = self.ui.tbv_flow.currentIndex().row()
        if row == -1:
            return
        vs = self.var_states[row]
        d = whichDependsOnIt(vs, self.var_states[row + 1:])
        if d is None:
            del self.var_states[row]
            self.model_flow.refresh()
        else:
            show_error_msg(parent=self, txt="Could not delete '" + vs.name + "'",
                           e="'" + d.name + "'" + " depends on it")

    @Slot()
    def fun_slider_dlt(self):
        row: int = self.ui.tb_slider.currentIndex().row()
        if row == -1:
            return
        v = self.ranged_vars[row]
        d = whichDependsOnIt(v, self.var_states)
        if d is None:
            del self.ranged_vars[row]
            self.manager_slider.deleteRow(row)
        else:
            show_error_msg(parent=self, txt="Could not delete '" + v.name + "'",
                           e="'" + d.name + "'" + " depends on it")

    @Slot(State)
    def new_state_created(self, st: State):
        self.var_states.append(st)
        self.model_flow.refresh()

    @Slot()
    def old_state_edited(self):
        self.model_flow.refresh()

    @Slot(Variable)
    def new_var_created(self, v: Variable):
        if v.hasRange():
            self.ranged_vars.append(v)
            self.manager_slider.newAddedLast()
            return

        self.var_states.append(v)
        self.model_flow.refresh()

    @Slot(Variable)
    def old_var_edited(self, v: Variable):
        if v.hasRange():
            self.manager_slider.refresh_at(v)

        self.model_flow.refresh()

    @Slot()
    def on_buttonBox_accepted(self):
        name: str = self.ui.ln_name.text()
        desc: str = self.ui.pte_desc.toPlainText()
        if not self.ranged_vars and not self.var_states:
            self.statusBar().showMessage("Nothing to save, define at least one state or variable")
            return
        if not name:
            self.ui.ln_name.setStyleSheet("border: 2px solid red")
            self.ui.ln_name.setFocus()
            self.statusBar().showMessage("Name Can't be Empty")

            def noRed():
                self.ui.ln_name.setStyleSheet("")
                self.ui.ln_name.textChanged.disconnect(noRed)
            self.ui.ln_name.textChanged.connect(noRed)
            return
        if self.edit is None:
            flow = Flow(name=name, fluids=self.fluids, var_states=self.var_states, ranged_vars=self.ranged_vars,
                        desc=desc)
            self.flow_created.emit(flow)
        else:
            self.edit.edit(name=name, fluids=self.fluids, var_states=self.var_states, ranged_vars=self.ranged_vars,
                           desc=desc)
            self.flow_edited.emit()

        self.close()

    @Slot()
    def on_buttonBox_rejected(self):
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.window_closed.emit(self)

    def setup_table_stretch(self):
        tables = (self.ui.tbv_states, self.ui.tbv_vars, self.ui.tb_slider)
        for table in tables:
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tbv_flow.horizontalHeader().setStretchLastSection(True)

    def setupFluidsLabel(self):
        self.ui.lb_fluids.setText(", ".join(self.fluids))
