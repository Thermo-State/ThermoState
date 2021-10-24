from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from UI.Qt_custom import KittyTable
from UI.Qt_custom import KittyList

from  . import images_rc
from  . import formula_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(775, 615)
        MainWindow.setMinimumSize(QSize(700, 0))
        icon = QIcon()
        icon.addFile(u":/png/Resources/TS-bold.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"#lb_input, #lb_history, #lb_adv_calc, #lb_graph {text-align: right; background-color :rgba(85, 170, 255, 100); font: 12pt; border: 2px solid green;}\n"
"")
        self.actionClearCurrFluid = QAction(MainWindow)
        self.actionClearCurrFluid.setObjectName(u"actionClearCurrFluid")
        self.actionClearAllFluids = QAction(MainWindow)
        self.actionClearAllFluids.setObjectName(u"actionClearAllFluids")
        self.actionSI = QAction(MainWindow)
        self.actionSI.setObjectName(u"actionSI")
        self.actionSI.setCheckable(True)
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.actionEnglish.setCheckable(True)
        self.actionDefault = QAction(MainWindow)
        self.actionDefault.setObjectName(u"actionDefault")
        self.actionDefault.setCheckable(True)
        self.actionCustomize = QAction(MainWindow)
        self.actionCustomize.setObjectName(u"actionCustomize")
        self.actionCustomize.setCheckable(True)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionClearSelected = QAction(MainWindow)
        self.actionClearSelected.setObjectName(u"actionClearSelected")
        self.actionWebsite = QAction(MainWindow)
        self.actionWebsite.setObjectName(u"actionWebsite")
        self.actionResetOrder = QAction(MainWindow)
        self.actionResetOrder.setObjectName(u"actionResetOrder")
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.vl_central_wgt = QVBoxLayout(self.centralwidget)
        self.vl_central_wgt.setObjectName(u"vl_central_wgt")
        self.wgt_inp_graph = QWidget(self.centralwidget)
        self.wgt_inp_graph.setObjectName(u"wgt_inp_graph")
        self.hl_wgt_inp_graph = QHBoxLayout(self.wgt_inp_graph)
        self.hl_wgt_inp_graph.setObjectName(u"hl_wgt_inp_graph")
        self.wgt_inp_adv = QWidget(self.wgt_inp_graph)
        self.wgt_inp_adv.setObjectName(u"wgt_inp_adv")
        self.vl_wgt_adv = QVBoxLayout(self.wgt_inp_adv)
        self.vl_wgt_adv.setObjectName(u"vl_wgt_adv")
        self.lb_input = QLabel(self.wgt_inp_adv)
        self.lb_input.setObjectName(u"lb_input")
        self.lb_input.setAlignment(Qt.AlignCenter)

        self.vl_wgt_adv.addWidget(self.lb_input)

        self.gl_input = QGridLayout()
        self.gl_input.setObjectName(u"gl_input")
        self.cb_unit_1 = QComboBox(self.wgt_inp_adv)
        self.cb_unit_1.setObjectName(u"cb_unit_1")

        self.gl_input.addWidget(self.cb_unit_1, 1, 2, 1, 1)

        self.cb_input_1 = QComboBox(self.wgt_inp_adv)
        self.cb_input_1.setObjectName(u"cb_input_1")

        self.gl_input.addWidget(self.cb_input_1, 1, 0, 1, 1)

        self.btn_fluid_info = QPushButton(self.wgt_inp_adv)
        self.btn_fluid_info.setObjectName(u"btn_fluid_info")

        self.gl_input.addWidget(self.btn_fluid_info, 0, 0, 1, 1)

        self.btn_add_fluid = QPushButton(self.wgt_inp_adv)
        self.btn_add_fluid.setObjectName(u"btn_add_fluid")

        self.gl_input.addWidget(self.btn_add_fluid, 0, 2, 1, 1)

        self.dspin_input_1 = QDoubleSpinBox(self.wgt_inp_adv)
        self.dspin_input_1.setObjectName(u"dspin_input_1")
        self.dspin_input_1.setDecimals(6)
        self.dspin_input_1.setMinimum(-10000000.000000000000000)
        self.dspin_input_1.setMaximum(99990000.000000000000000)

        self.gl_input.addWidget(self.dspin_input_1, 1, 1, 1, 1)

        self.cb_input_fluid = QComboBox(self.wgt_inp_adv)
        self.cb_input_fluid.setObjectName(u"cb_input_fluid")

        self.gl_input.addWidget(self.cb_input_fluid, 0, 1, 1, 1)

        self.cb_input_2 = QComboBox(self.wgt_inp_adv)
        self.cb_input_2.setObjectName(u"cb_input_2")

        self.gl_input.addWidget(self.cb_input_2, 2, 0, 1, 1)

        self.dspin_input_2 = QDoubleSpinBox(self.wgt_inp_adv)
        self.dspin_input_2.setObjectName(u"dspin_input_2")
        self.dspin_input_2.setDecimals(6)
        self.dspin_input_2.setMinimum(-10000000.000000000000000)
        self.dspin_input_2.setMaximum(99990000.000000000000000)

        self.gl_input.addWidget(self.dspin_input_2, 2, 1, 1, 1)

        self.cb_unit_2 = QComboBox(self.wgt_inp_adv)
        self.cb_unit_2.setObjectName(u"cb_unit_2")

        self.gl_input.addWidget(self.cb_unit_2, 2, 2, 1, 1)

        self.gl_input.setColumnStretch(0, 1)
        self.gl_input.setColumnStretch(1, 2)
        self.gl_input.setColumnStretch(2, 1)

        self.vl_wgt_adv.addLayout(self.gl_input)

        self.btn_calculate = QPushButton(self.wgt_inp_adv)
        self.btn_calculate.setObjectName(u"btn_calculate")

        self.vl_wgt_adv.addWidget(self.btn_calculate)

        self.lb_adv_calc = QLabel(self.wgt_inp_adv)
        self.lb_adv_calc.setObjectName(u"lb_adv_calc")
        self.lb_adv_calc.setAlignment(Qt.AlignCenter)

        self.vl_wgt_adv.addWidget(self.lb_adv_calc)

        self.lv_flowList = KittyList(self.wgt_inp_adv)
        self.lv_flowList.setObjectName(u"lv_flowList")
        font = QFont()
        font.setPointSize(12)
        self.lv_flowList.setFont(font)
        self.lv_flowList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lv_flowList.setSelectionRectVisible(True)

        self.vl_wgt_adv.addWidget(self.lv_flowList)

        self.hl_flow_btns = QHBoxLayout()
        self.hl_flow_btns.setObjectName(u"hl_flow_btns")
        self.btn_new_flow = QPushButton(self.wgt_inp_adv)
        self.btn_new_flow.setObjectName(u"btn_new_flow")

        self.hl_flow_btns.addWidget(self.btn_new_flow)

        self.btn_delete_flow = QPushButton(self.wgt_inp_adv)
        self.btn_delete_flow.setObjectName(u"btn_delete_flow")

        self.hl_flow_btns.addWidget(self.btn_delete_flow)


        self.vl_wgt_adv.addLayout(self.hl_flow_btns)

        self.vl_wgt_adv.setStretch(1, 1)

        self.hl_wgt_inp_graph.addWidget(self.wgt_inp_adv)

        self.wgt_graph = QWidget(self.wgt_inp_graph)
        self.wgt_graph.setObjectName(u"wgt_graph")
        self.vl_wgt_graph = QVBoxLayout(self.wgt_graph)
        self.vl_wgt_graph.setObjectName(u"vl_wgt_graph")
        self.lb_graph = QLabel(self.wgt_graph)
        self.lb_graph.setObjectName(u"lb_graph")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_graph.sizePolicy().hasHeightForWidth())
        self.lb_graph.setSizePolicy(sizePolicy)
        self.lb_graph.setAlignment(Qt.AlignCenter)

        self.vl_wgt_graph.addWidget(self.lb_graph)

        self.tab_wgt_graph = QTabWidget(self.wgt_graph)
        self.tab_wgt_graph.setObjectName(u"tab_wgt_graph")

        self.vl_wgt_graph.addWidget(self.tab_wgt_graph)


        self.hl_wgt_inp_graph.addWidget(self.wgt_graph)

        self.hl_wgt_inp_graph.setStretch(0, 1)
        self.hl_wgt_inp_graph.setStretch(1, 1)

        self.vl_central_wgt.addWidget(self.wgt_inp_graph)

        self.wgt_hist = QWidget(self.centralwidget)
        self.wgt_hist.setObjectName(u"wgt_hist")
        self.verticalLayout_2 = QVBoxLayout(self.wgt_hist)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.hl_hist_1 = QHBoxLayout()
        self.hl_hist_1.setObjectName(u"hl_hist_1")
        self.lb_history = QLabel(self.wgt_hist)
        self.lb_history.setObjectName(u"lb_history")
        self.lb_history.setAlignment(Qt.AlignCenter)

        self.hl_hist_1.addWidget(self.lb_history)

        self.hl_hist_1.setStretch(0, 4)

        self.verticalLayout_2.addLayout(self.hl_hist_1)

        self.hl_hist_2 = QHBoxLayout()
        self.hl_hist_2.setObjectName(u"hl_hist_2")
        self.tbv_calc_hist = KittyTable(self.wgt_hist)
        self.tbv_calc_hist.setObjectName(u"tbv_calc_hist")
        self.tbv_calc_hist.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbv_calc_hist.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.hl_hist_2.addWidget(self.tbv_calc_hist)

        self.tbv_output = KittyTable(self.wgt_hist)
        self.tbv_output.setObjectName(u"tbv_output")
        self.tbv_output.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbv_output.setTabKeyNavigation(False)
        self.tbv_output.setProperty("showDropIndicator", False)
        self.tbv_output.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbv_output.horizontalHeader().setVisible(False)

        self.hl_hist_2.addWidget(self.tbv_output)

        self.hl_hist_2.setStretch(0, 2)
        self.hl_hist_2.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.hl_hist_2)


        self.vl_central_wgt.addWidget(self.wgt_hist)

        self.lb_update = QLabel(self.centralwidget)
        self.lb_update.setObjectName(u"lb_update")
        self.lb_update.setStyleSheet(u"color: blue")

        self.vl_central_wgt.addWidget(self.lb_update)

        self.vl_central_wgt.setStretch(0, 2)
        self.vl_central_wgt.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 775, 22))
        self.menuHistory = QMenu(self.menubar)
        self.menuHistory.setObjectName(u"menuHistory")
        self.menuHistory.setToolTipsVisible(True)
        self.menuUnit = QMenu(self.menubar)
        self.menuUnit.setObjectName(u"menuUnit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuFlow = QMenu(self.menubar)
        self.menuFlow.setObjectName(u"menuFlow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFlow.menuAction())
        self.menubar.addAction(self.menuHistory.menuAction())
        self.menubar.addAction(self.menuUnit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHistory.addSeparator()
        self.menuHistory.addAction(self.actionClearSelected)
        self.menuHistory.addAction(self.actionClearCurrFluid)
        self.menuHistory.addAction(self.actionClearAllFluids)
        self.menuHistory.addSeparator()
        self.menuHistory.addAction(self.actionResetOrder)
        self.menuUnit.addAction(self.actionSI)
        self.menuUnit.addAction(self.actionEnglish)
        self.menuUnit.addAction(self.actionDefault)
        self.menuUnit.addSeparator()
        self.menuUnit.addAction(self.actionCustomize)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionWebsite)
        self.menuFlow.addAction(self.actionImport)
        self.menuFlow.addAction(self.actionExport)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ThermoState", None))
        self.actionClearCurrFluid.setText(QCoreApplication.translate("MainWindow", u"Clear Current Fluid", None))
#if QT_CONFIG(tooltip)
        self.actionClearCurrFluid.setToolTip(QCoreApplication.translate("MainWindow", u"Remove history for current fluid", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionClearCurrFluid.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionClearAllFluids.setText(QCoreApplication.translate("MainWindow", u"Clear all Fluids", None))
#if QT_CONFIG(tooltip)
        self.actionClearAllFluids.setToolTip(QCoreApplication.translate("MainWindow", u"Remove history for all fluids", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionClearAllFluids.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionSI.setText(QCoreApplication.translate("MainWindow", u"SI", None))
        self.actionEnglish.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.actionDefault.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.actionCustomize.setText(QCoreApplication.translate("MainWindow", u"Customize", None))
#if QT_CONFIG(tooltip)
        self.actionCustomize.setToolTip(QCoreApplication.translate("MainWindow", u"Customize unit for each property", None))
#endif // QT_CONFIG(tooltip)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionClearSelected.setText(QCoreApplication.translate("MainWindow", u"Clear Selected", None))
#if QT_CONFIG(tooltip)
        self.actionClearSelected.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected result from history", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionClearSelected.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionWebsite.setText(QCoreApplication.translate("MainWindow", u"Website", None))
        self.actionResetOrder.setText(QCoreApplication.translate("MainWindow", u"Reset Order", None))
#if QT_CONFIG(tooltip)
        self.actionResetOrder.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the order of state number", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionResetOrder.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
#if QT_CONFIG(tooltip)
        self.actionImport.setToolTip(QCoreApplication.translate("MainWindow", u"Import from file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionImport.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
#if QT_CONFIG(tooltip)
        self.actionExport.setToolTip(QCoreApplication.translate("MainWindow", u"Export to a file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionExport.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(statustip)
        self.lb_input.setStatusTip(QCoreApplication.translate("MainWindow", u"To define a state, You need to specify two independent, intensive properties. Use Quality 0 or 1 for saturated state", None))
#endif // QT_CONFIG(statustip)
        self.lb_input.setText(QCoreApplication.translate("MainWindow", u"Input", None))
        self.btn_fluid_info.setText(QCoreApplication.translate("MainWindow", u"Fluid info", None))
#if QT_CONFIG(statustip)
        self.btn_add_fluid.setStatusTip(QCoreApplication.translate("MainWindow", u"Add or Remove fluid(s). ", None))
#endif // QT_CONFIG(statustip)
        self.btn_add_fluid.setText(QCoreApplication.translate("MainWindow", u"More fluids", None))
#if QT_CONFIG(statustip)
        self.btn_calculate.setStatusTip(QCoreApplication.translate("MainWindow", u"Solve for the given input", None))
#endif // QT_CONFIG(statustip)
        self.btn_calculate.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
#if QT_CONFIG(statustip)
        self.lb_adv_calc.setStatusTip(QCoreApplication.translate("MainWindow", u"Flow is a chain of calculations of related states. Thermodynamic cycles can be modeled with flow. Flow can be imported / exported", None))
#endif // QT_CONFIG(statustip)
        self.lb_adv_calc.setText(QCoreApplication.translate("MainWindow", u"Flow", None))
#if QT_CONFIG(statustip)
        self.btn_new_flow.setStatusTip(QCoreApplication.translate("MainWindow", u"Define a new Flow.", None))
#endif // QT_CONFIG(statustip)
        self.btn_new_flow.setText(QCoreApplication.translate("MainWindow", u"Define new", None))
#if QT_CONFIG(statustip)
        self.btn_delete_flow.setStatusTip(QCoreApplication.translate("MainWindow", u"Delete selected flow. This action is irreversible", None))
#endif // QT_CONFIG(statustip)
        self.btn_delete_flow.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(statustip)
        self.lb_graph.setStatusTip(QCoreApplication.translate("MainWindow", u"States will be plotted here. You can switch between different diagrams.", None))
#endif // QT_CONFIG(statustip)
        self.lb_graph.setText(QCoreApplication.translate("MainWindow", u"Diagram", None))
#if QT_CONFIG(statustip)
        self.lb_history.setStatusTip(QCoreApplication.translate("MainWindow", u"Results are stored here. You can delete history & set your preferred units from menu. Double click on a value to use it as input", None))
#endif // QT_CONFIG(statustip)
        self.lb_history.setText(QCoreApplication.translate("MainWindow", u"History", None))
        self.lb_update.setText("")
        self.menuHistory.setTitle(QCoreApplication.translate("MainWindow", u"History", None))
        self.menuUnit.setTitle(QCoreApplication.translate("MainWindow", u"Unit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuFlow.setTitle(QCoreApplication.translate("MainWindow", u"Flow", None))
    # retranslateUi

