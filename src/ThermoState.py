import datetime
import os
import pickle
import sys
import traceback
from contextlib import suppress
from typing import List, Type, TypedDict, Optional, Dict, Tuple

from PySide2.QtCore import QUrl, Slot, Qt
from PySide2.QtGui import QDesktopServices, QCloseEvent, QPixmap
from PySide2.QtWidgets import QMainWindow, QApplication, QActionGroup, QAction, QHeaderView, QFileDialog, QSplashScreen
from pyqtgraph import setConfigOptions, TextItem, PlotWidget, PlotCurveItem, ScatterPlotItem, mkPen

from AboutDialog import AboutDialog
from FlowWindow import FlowWindow
from FluidInfoDialog import FluidInfoDialog
from FluidsDialog import FluidsDialog
from Model.BaseProperty import BaseProperty, UNIT
from Model.CoolPropInterface import get_available_input_properties, get_other_input_properties, \
    get_x_y, list_diagrams, Fluids
from Model.PureSubstances import PureState, StateNoManager
from Model.VarState import Flow, flowImporter, flowExporter
from Model.ViewModels import OutTableModel, HistoryTableModel
from Model.viewModels2 import FlowListModel
from ProgramVariables import ServerInfo, ProgramInfo, Path
from UI import images_rc  # noqa
from UI.Qt_custom import MyLineEdit, show_error_msg
from UI.UI_MainWindow import Ui_MainWindow
from UnitDialog import set_unit, UnitDialog, load_custom_units

setConfigOptions(background="w", foreground="k")


class Settings(TypedDict):
    unit_selected: str
    current_fluid: str
    run_count: int
    update_check_count: int
    last_update_check: Optional[datetime.date]
    update_available: bool
    last_path: str


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plots: List[PlotWidget] = []

        self.unit_action_grp = QActionGroup(self.ui.menuUnit)
        self.unit_actions: List[QAction] = []
        self.setupCustomUI()
        self.childFlowWindows: List[QMainWindow] = []

        self.states: Dict[str, List[PureState]] = {}
        self.states_plot: Dict[str, Dict[int, List[Tuple[ScatterPlotItem, TextItem]]]] = {}
        self.flows: List[Flow] = []

        self.fluids: List[str] = Fluids.default
        self.settings: Settings = Settings(unit_selected=UNIT.DEFAULT,
                                           current_fluid="Water",
                                           run_count=0,
                                           update_check_count=0,
                                           last_update_check=None,
                                           update_available=False,
                                           last_path="")
        self.load_session()
        self.custom_units_session: List[str] = []
        self.set_update_status()

        if self.settings['run_count'] == 0:
            from Model.Examples import exFlows, exStates
            self.states = exStates
            self.flows = [flowImporter(json_str=exFlow, build=ProgramInfo.build) for exFlow in exFlows]

        self.model_outTable = OutTableModel()
        self.model_histTable = HistoryTableModel()
        self.model_flowList = FlowListModel(self.flows)
        self.ui.tbv_calc_hist.setModel(self.model_histTable)
        self.ui.tbv_output.setModel(self.model_outTable)
        self.ui.lv_flowList.setModel(self.model_flowList)
        self.ui.tbv_calc_hist.selectionModel().selectionChanged.connect(self.on_tbv_calc_hist_selectionChanged)

        self.stateNoManager = StateNoManager(self.states)
        self.setup_cb_input_fluid()

        if self.register:
            # Removed all codes related to Update Check since it is not necessary for scripts
            pass

    @Slot()
    def on_btn_fluid_info_clicked(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        fid = FluidInfoDialog(self, fluid)
        fid.exec_()

    @Slot()
    def on_btn_add_fluid_clicked(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        self.settings["current_fluid"] = fluid
        fd: FluidsDialog = FluidsDialog(self, fluids=self.fluids)
        if fd.exec_():
            self.setup_cb_input_fluid()

    @Slot()
    def on_btn_calculate_clicked(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        class_property_1: Type[BaseProperty] = self.ui.cb_input_1.currentData()
        class_property_2: Type[BaseProperty] = self.ui.cb_input_2.currentData()

        value_prop_1: float = self.ui.dspin_input_1.value()
        value_prop_2: float = self.ui.dspin_input_2.value()

        unit_prop_1: str = self.ui.cb_unit_1.currentText()
        unit_prop_2: str = self.ui.cb_unit_2.currentText()

        try:
            obj_property_1 = class_property_1(value=value_prop_1, unit=unit_prop_1)
            obj_property_2 = class_property_2(value=value_prop_2, unit=unit_prop_2)

            current_state = PureState(fluid, obj_property_1, obj_property_2, no=self.stateNoManager.get_no(fluid))
        except Exception as e_calc:
            show_error_msg(parent=self, txt="CoolProp encountered an Error. Check if the inputs are valid",
                           e=str(e_calc))
            return

        self.states[fluid].append(current_state)
        self.stateNoManager.increment(fluid)

        self.model_histTable.refresh()
        self.newStateAdded()
        self.ui.tbv_calc_hist.selectRow(self.states[fluid].index(current_state))

    @Slot()
    def on_btn_new_flow_clicked(self):
        fw = FlowWindow(None)
        self.childFlowWindows.append(fw)
        fw.window_closed.connect(self.childFlowWindowClosed)
        fw.flow_created.connect(self.new_flow_created)
        fw.show()
        self.showMinimized()

    @Slot()
    def on_btn_delete_flow_clicked(self):
        i: int = self.ui.lv_flowList.currentIndex().row()
        if i == -1 or self.model_flowList.rowCount() == 0:
            return
        self.flows.pop(i)
        self.model_flowList.refresh()

    @Slot()
    def on_actionImport_triggered(self):
        path: str = self.settings['last_path'] if self.settings['last_path'] else Path.home
        filePath, _ = QFileDialog.getOpenFileName(self, caption="Import Flow from", dir=path,
                                                  filter="Flow File (*.ts-flow)")
        if filePath:
            self.settings['last_path'] = os.path.dirname(filePath)
            try:
                with open(filePath, "r", encoding="utf-8") as f:
                    json_str: str = f.read()
                    flow = flowImporter(json_str=json_str, build=ProgramInfo.build)

                    self.flows.append(flow)
                    self.model_flowList.refresh()

            except Exception as e:
                show_error_msg(txt="An Error Occurred while importing the file", e=str(e))

    @Slot()
    def on_actionExport_triggered(self):
        if self.model_flowList.rowCount() == 0:
            show_error_msg(e="Nothing to export. Define new flow first")
            return
        i: int = self.ui.lv_flowList.currentIndex().row()
        if i == -1:
            show_error_msg(e="Select a flow first to export")
            return
        flow: Flow = self.flows[i]
        json_str: str = flowExporter(flow=flow, build=ProgramInfo.build)

        filename: str = f"{flow.name}.ts-flow"
        path: str = os.path.join(self.settings['last_path'], filename) \
            if self.settings['last_path'] else os.path.join(Path.home, filename)
        filePath, _ = QFileDialog.getSaveFileName(self, caption="Export Flow as", dir=path,
                                                  filter="Flow File (*.ts-flow)")
        if filePath:
            self.settings['last_path'] = os.path.dirname(filePath)
            try:
                with open(filePath, "w", encoding="utf-8") as f:
                    f.write(json_str)
            except Exception as e:
                show_error_msg(e=str(e), details=traceback.format_exc())

    @Slot()
    def on_actionResetOrder_triggered(self):
        self.stateNoManager.resetOrder(self.ui.cb_input_fluid.currentText())
        self.model_histTable.headerDataChanged.emit(Qt.Horizontal, 0, self.model_histTable.columnCount() - 1)
        self.reorder_plot_states()

    @Slot()
    def on_actionClearSelected_triggered(self):
        if self.ui.tbv_calc_hist.selectionModel().hasSelection():
            i: int = self.ui.tbv_calc_hist.selectionModel().currentIndex().row()
            rc: int = self.model_histTable.rowCount()
            fluid: str = self.ui.cb_input_fluid.currentText()

            self.states[fluid].pop(i)
            self.stateNoManager.refreshFluid(fluid)
            self.setup_hist_table_data()
            for plot_index in range(len(list_diagrams)):
                sc_plot, txt_plot = self.states_plot[fluid][plot_index].pop(i)
                self.plots[plot_index].removeItem(sc_plot)
                self.plots[plot_index].removeItem(txt_plot)

            if i != rc - 2 or rc != 1:
                self.ui.tbv_calc_hist.selectRow(i)

    @Slot()
    def on_actionClearCurrFluid_triggered(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        self.states[fluid] = []
        self.stateNoManager.refreshFluid(fluid)
        self.setup_hist_table_data()
        self.remove_state_plots()
        self.ui.statusbar.showMessage("Cleared Calculation History for " + fluid)

    @Slot()
    def on_actionClearAllFluids_triggered(self):
        for key in self.states.keys():
            self.states[key] = []
        self.stateNoManager.refresh()
        self.setup_hist_table_data()
        self.remove_state_plots()
        self.ui.statusbar.showMessage("Cleared Calculation History for " + str(len(self.states)) + " Fluid(s)")

    @Slot()
    def on_actionAbout_triggered(self):
        about_dialog: AboutDialog = AboutDialog(self)
        about_dialog.exec_()

    @Slot()
    def on_actionWebsite_triggered(self):
        QDesktopServices.openUrl(QUrl(ServerInfo.website))

    @Slot(QAction)
    def on_unit_action_grp_triggered(self, action: QAction):
        unit = action.text()
        if unit != UNIT.CUSTOM:
            set_unit(action.text())
            self.settings['unit_selected'] = unit
            self.emit_unit_changed()
            self.ui.statusbar.showMessage("Unit has been set to " + unit)
        else:
            ud: UnitDialog = UnitDialog(self)
            if ud.exec_():
                self.custom_units_session = ud.custom_units
                self.emit_unit_changed()
                self.settings['unit_selected'] = unit
                self.ui.statusbar.showMessage("Customized units are applied")
            else:
                self.set_unit_checked()

    @Slot()
    def on_tbv_calc_hist_doubleClicked(self):
        itemTexts = [self.ui.cb_input_1.itemText(i) for i in range(self.ui.cb_input_1.count())]
        prop: BaseProperty = self.model_histTable.get_property(self.ui.tbv_calc_hist.currentIndex())
        if prop.label not in itemTexts:
            return
        if self.ui.cb_input_2.currentText() == prop.label:
            self.ui.cb_input_2.setCurrentText(prop.label)
            self.ui.dspin_input_2.setValue(prop.in_unit(self.ui.cb_unit_2.currentText()))
        else:
            self.ui.cb_input_1.setCurrentText(prop.label)
            self.ui.dspin_input_1.setValue(prop.in_unit(self.ui.cb_unit_1.currentText()))

    @Slot()
    def on_lv_flowList_doubleClicked(self):
        i: int = self.ui.lv_flowList.currentIndex().row()
        fw = FlowWindow(None, edit=self.flows[i])
        self.childFlowWindows.append(fw)
        fw.window_closed.connect(self.childFlowWindowClosed)
        fw.flow_created.connect(self.old_flow_edited)
        fw.show()
        self.showMinimized()

    @Slot()
    def on_tbv_calc_hist_selectionChanged(self):
        if self.ui.tbv_calc_hist.selectionModel().hasSelection():
            fluid: str = self.ui.cb_input_fluid.currentText()
            i: int = self.ui.tbv_calc_hist.selectionModel().currentIndex().row()
            self.model_outTable.changeData(self.states[fluid][i].get_other_properties())

    @Slot()
    def on_cb_input_fluid_currentIndexChanged(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        if fluid == "":
            return
        self.setup_cb_input_1()
        self.setup_hist_table_data()
        self.setup_graph()
        self.ui.btn_fluid_info.setStatusTip(f"Show information on '{fluid}'")

    @Slot()
    def on_cb_input_1_currentIndexChanged(self):
        self.setup_cb_input_2()
        self.setup_cb_unit_1()

    @Slot()
    def on_cb_input_2_currentIndexChanged(self):
        self.setup_cb_unit_2()

    @Slot(QMainWindow)
    def childFlowWindowClosed(self, fw):
        self.childFlowWindows.remove(fw)
        self.showNormal()

    @Slot(Flow)
    def new_flow_created(self, flow: Flow):
        self.flows.append(flow)
        self.model_flowList.refresh()

    @Slot()
    def old_flow_edited(self):
        self.model_flowList.refresh()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.childFlowWindows:
            event.ignore()
            show_error_msg(txt="Window couldn't be closed",
                           e="Save your work and close Flow window(s) first")
        else:
            self.save_session()
            event.accept()

    def load_session(self):
        if not os.path.exists(Path.data_dir):
            return

        if os.path.exists(Path.history):
            with open(Path.history, "rb") as f:
                self.states: Dict[str, List[PureState]] = pickle.load(f)
                self.fluids: List[str] = list(self.states.keys())

        if os.path.exists(Path.flows):
            with open(Path.flows, "rb") as f:
                self.flows: List[Flow] = pickle.load(f)

        if os.path.exists(Path.settings):
            with open(Path.settings, "rb") as f:
                self.settings: Settings = pickle.load(f)

        unit_selected: str = self.settings["unit_selected"]
        if unit_selected == UNIT.CUSTOM:
            if os.path.exists(Path.unit):
                with open(Path.unit, "rb") as f:
                    custom_units = pickle.load(f)
                load_custom_units(custom_units)
            else:
                self.settings["unit_selected"] = UNIT.DEFAULT
        else:
            if unit_selected != UNIT.DEFAULT:
                set_unit(unit_selected)

        self.set_unit_checked()

    def save_session(self):
        if not os.path.exists(Path.data_dir):
            os.makedirs(Path.data_dir)

        self.settings["current_fluid"] = self.ui.cb_input_fluid.currentText()
        self.settings["unit_selected"] = self.unit_action_grp.checkedAction().text()
        self.settings['run_count'] = self.settings['run_count'] + 1

        with suppress(Exception):
            with open(Path.settings, "wb") as f:
                pickle.dump(self.settings, f, protocol=pickle.HIGHEST_PROTOCOL)
            with open(Path.history, "wb") as f:
                pickle.dump(self.states, f, protocol=pickle.HIGHEST_PROTOCOL)
            with open(Path.flows, "wb") as f:
                pickle.dump(self.flows, f, protocol=pickle.HIGHEST_PROTOCOL)

        if self.settings["unit_selected"] == UNIT.CUSTOM:
            if len(self.custom_units_session) != 0:
                with suppress(Exception):
                    with open(Path.unit, "wb") as f:
                        pickle.dump(self.custom_units_session, f, protocol=pickle.HIGHEST_PROTOCOL)

    def setupCustomUI(self):
        self.unit_actions = [self.ui.actionSI, self.ui.actionEnglish, self.ui.actionDefault, self.ui.actionCustomize]
        for unit_action in self.unit_actions:
            self.unit_action_grp.addAction(unit_action)

        self.unit_action_grp.setExclusive(True)

        self.ui.actionDefault.setChecked(True)
        self.unit_action_grp.triggered.connect(self.on_unit_action_grp_triggered)

        self.ui.dspin_input_1.setLineEdit(MyLineEdit())
        self.ui.dspin_input_2.setLineEdit(MyLineEdit())

        self.ui.tbv_output.setSpan(0, 0, 1, 2)
        self.ui.tbv_output.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tbv_calc_hist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for ls in list_diagrams:
            label: str = ls[0].symbol + ls[1].symbol
            plot_wgt = PlotWidget()
            plot_wgt.getPlotItem().setMenuEnabled(False)
            self.plots.append(plot_wgt)
            self.ui.tab_wgt_graph.addTab(plot_wgt, label)

    def setup_states_dict(self):
        keys = list(self.states.keys())
        for fluid in self.fluids:
            if fluid not in keys:
                self.states[fluid] = []

        for key in keys:
            if key not in self.fluids:
                del self.states[key]
        self.stateNoManager.fluidChanged()

    def setup_cb_input_fluid(self):
        self.setup_states_dict()

        self.ui.cb_input_fluid.clear()
        keys = self.states.keys()

        for fluid in keys:
            self.ui.cb_input_fluid.addItem(fluid)

        curr_fluid = self.settings['current_fluid']
        if curr_fluid in keys:
            self.ui.cb_input_fluid.setCurrentText(curr_fluid)

    def setup_cb_input_1(self):
        fluid: str = self.ui.cb_input_fluid.currentText()

        self.ui.cb_input_1.clear()
        for class_property in get_available_input_properties(fluid):
            self.ui.cb_input_1.addItem(class_property.label, class_property)

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

    def setup_cb_unit_1(self):
        """need to be called by the slot that handles cb_input_1"""
        class_property: BaseProperty = self.ui.cb_input_1.currentData()
        if class_property is None:
            return
        self.ui.cb_unit_1.clear()
        for unit in class_property.units:
            unit: str
            self.ui.cb_unit_1.addItem(unit)
        self.ui.cb_unit_1.setCurrentText(class_property.get_curr_unit())

    def setup_cb_unit_2(self):
        """need to be called by the slot that handles cb_input_2"""
        class_property: Type[BaseProperty] = self.ui.cb_input_2.currentData()
        if class_property is None:
            return

        self.ui.cb_unit_2.clear()
        for unit in class_property.units:
            unit: str
            self.ui.cb_unit_2.addItem(unit)
        self.ui.cb_unit_2.setCurrentText(class_property.get_curr_unit())

    def setup_hist_table_data(self):
        fluid: str = self.ui.cb_input_fluid.currentText()

        self.ui.tbv_calc_hist.selectionModel().clearSelection()
        self.model_histTable.changeData(self.states[fluid])
        rc: int = self.model_histTable.rowCount()
        if rc != 0:
            self.ui.tbv_calc_hist.selectRow(rc - 1)
        else:
            self.model_outTable.empty()

    def setup_graph(self):
        fluid: str = self.ui.cb_input_fluid.currentText()

        states = self.states[fluid]
        states_plot: Dict[int, List[Tuple[ScatterPlotItem, TextItem]]] = {}

        for i, ls in enumerate(list_diagrams):
            self.plots[i].clear()
            x_class, y_class = ls[1], ls[0]
            x_data, y_data = get_x_y(fluid, class_property_1=x_class, class_property_2=y_class)
            self.plots[i].enableAutoRange()
            self.plots[i].addItem(PlotCurveItem(x_data, y_data, pen=mkPen(color=(200, 200, 255), width=3)))
            self.plots[i].setLabel("bottom", text=f'{x_class.symbol} [{x_class.get_curr_unit()}]')
            self.plots[i].setLabel("left", text=f'{y_class.symbol} [{y_class.get_curr_unit()}]')

            states_plot[i] = []
            for state in states:
                x: float = state.get_property(x_class).in_curr_unit()
                y: float = state.get_property(y_class).in_curr_unit()
                sc_plot = ScatterPlotItem(x=[x], y=[y], symbol='+', pen='r')
                txt_plot = TextItem(text=str(state.no), color='b')
                txt_plot.setPos(x, y)
                self.plots[i].addItem(sc_plot)
                self.plots[i].addItem(txt_plot)
                states_plot[i].append((sc_plot, txt_plot))

        self.states_plot[fluid] = states_plot

    def reorder_plot_states(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        for plot_index in range(len(list_diagrams)):
            for i, tup in enumerate(self.states_plot[fluid][plot_index]):
                sc_plot, txt_plot = tup
                txt_plot.setText(text=str(i + 1), color='b')

    def remove_state_plots(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        for plot_index in range(len(list_diagrams)):
            for sc_plot, txt_plot in self.states_plot[fluid][plot_index]:
                self.plots[plot_index].removeItem(sc_plot)
                self.plots[plot_index].removeItem(txt_plot)
            self.states_plot[fluid][plot_index].clear()

    def newStateAdded(self):
        fluid: str = self.ui.cb_input_fluid.currentText()
        state: PureState = self.states[fluid][-1]

        for i, ls in enumerate(list_diagrams):
            x_class, y_class = ls[1], ls[0]
            x: float = state.get_property(x_class).in_curr_unit()
            y: float = state.get_property(y_class).in_curr_unit()
            sc_plot = ScatterPlotItem(x=[x], y=[y], symbol='+', pen='r')
            txt_plot = TextItem(text=str(state.no), color='b')
            txt_plot.setPos(x, y)
            self.plots[i].addItem(sc_plot)
            self.plots[i].addItem(txt_plot)
            self.states_plot[fluid][i].append((sc_plot, txt_plot))

    def emit_unit_changed(self):
        self.model_histTable.refresh()
        self.model_outTable.refresh()
        self.ui.cb_unit_1.setCurrentText(self.ui.cb_input_1.currentData().get_curr_unit())
        self.ui.cb_unit_2.setCurrentText(self.ui.cb_input_2.currentData().get_curr_unit())
        self.setup_graph()

    def set_unit_checked(self):
        unit_selected: str = self.settings['unit_selected']

        for unit_action in self.unit_actions:
            if unit_selected == unit_action.text():
                unit_action.setChecked(True)
                break

    @property
    def register(self) -> bool:
        lr = self.settings.get('last_update_check')
        if lr is None:
            return True
        else:
            next_update = lr + datetime.timedelta(days=ServerInfo.register_interval_days)
            now = datetime.datetime.now().date()
            if now >= next_update:
                return True
            else:
                return False

    def set_update_status(self):
        if self.settings["update_available"]:
            self.ui.lb_update.setHidden(False)
            self.ui.lb_update.setText("A new version is available for download. More on Help > Website")
        else:
            self.ui.lb_update.setHidden(True)


def exceptionHook(exc_type, exc_value, tb):
    details = "".join(traceback.format_tb(tb)) + exc_type.__name__ + ": " + str(exc_value)
    show_error_msg(e="Please report bug to the developer. Open new issue and submit error details (copied)",
                   details=details)
    clipboard = QApplication.clipboard()
    clipboard.setText(details)
    url = QUrl(ServerInfo.issue_url)
    QDesktopServices.openUrl(url)
    sys.exit()


def main():
    pixmap = QPixmap(':/png/Resources/splash.png')
    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    splash.show()
    mainWindow: MainWindow = MainWindow()
    mainWindow.show()
    splash.finish(mainWindow)
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.excepthook = exceptionHook
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app: QApplication = QApplication(sys.argv)
    main()
