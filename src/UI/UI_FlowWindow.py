from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from UI.Qt_custom import KittyTable

from  . import images_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(733, 590)
        MainWindow.setMinimumSize(QSize(730, 550))
        icon = QIcon()
        icon.addFile(u":/png/Resources/TS-bold.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.wgt_name_desc = QWidget(self.widget)
        self.wgt_name_desc.setObjectName(u"wgt_name_desc")
        self.wgt_name_desc.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.verticalLayout_4 = QVBoxLayout(self.wgt_name_desc)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lb_name = QLabel(self.wgt_name_desc)
        self.lb_name.setObjectName(u"lb_name")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_name)

        self.ln_name = QLineEdit(self.wgt_name_desc)
        self.ln_name.setObjectName(u"ln_name")
        self.ln_name.setMaxLength(50)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ln_name)

        self.lb_desc = QLabel(self.wgt_name_desc)
        self.lb_desc.setObjectName(u"lb_desc")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_desc)

        self.pte_desc = QPlainTextEdit(self.wgt_name_desc)
        self.pte_desc.setObjectName(u"pte_desc")
        self.pte_desc.setMaximumSize(QSize(16777215, 50))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pte_desc)

        self.btn_edit_fluids = QPushButton(self.wgt_name_desc)
        self.btn_edit_fluids.setObjectName(u"btn_edit_fluids")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.btn_edit_fluids)

        self.lb_fluids = QLabel(self.wgt_name_desc)
        self.lb_fluids.setObjectName(u"lb_fluids")
        self.lb_fluids.setWordWrap(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lb_fluids)


        self.verticalLayout_4.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.label = QLabel(self.wgt_name_desc)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.tb_slider = QTableWidget(self.wgt_name_desc)
        self.tb_slider.setObjectName(u"tb_slider")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_slider.sizePolicy().hasHeightForWidth())
        self.tb_slider.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(160, 160, 160, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush1)
        brush2 = QBrush(QColor(160, 160, 160, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush1)
        self.tb_slider.setPalette(palette)
        self.tb_slider.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tb_slider.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tb_slider.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tb_slider.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_slider.setShowGrid(False)
        self.tb_slider.horizontalHeader().setVisible(False)
        self.tb_slider.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.tb_slider)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.chb_auto_calc = QCheckBox(self.wgt_name_desc)
        self.chb_auto_calc.setObjectName(u"chb_auto_calc")

        self.horizontalLayout_4.addWidget(self.chb_auto_calc)

        self.btn_calc = QPushButton(self.wgt_name_desc)
        self.btn_calc.setObjectName(u"btn_calc")

        self.horizontalLayout_4.addWidget(self.btn_calc)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(3, 2)

        self.horizontalLayout.addWidget(self.wgt_name_desc)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_2 = QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lb_flow = QLabel(self.widget_4)
        self.lb_flow.setObjectName(u"lb_flow")

        self.verticalLayout_2.addWidget(self.lb_flow)

        self.tbv_flow = QTableView(self.widget_4)
        self.tbv_flow.setObjectName(u"tbv_flow")
        self.tbv_flow.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tbv_flow.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbv_flow.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_2.addWidget(self.tbv_flow)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_new_var = QPushButton(self.widget_4)
        self.btn_new_var.setObjectName(u"btn_new_var")

        self.horizontalLayout_2.addWidget(self.btn_new_var)

        self.btn_new_state = QPushButton(self.widget_4)
        self.btn_new_state.setObjectName(u"btn_new_state")

        self.horizontalLayout_2.addWidget(self.btn_new_state)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addWidget(self.widget_4)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.tbv_states = KittyTable(self.widget_2)
        self.tbv_states.setObjectName(u"tbv_states")
        self.tbv_states.setSelectionMode(QAbstractItemView.NoSelection)

        self.horizontalLayout_5.addWidget(self.tbv_states)

        self.tbv_vars = KittyTable(self.widget_2)
        self.tbv_vars.setObjectName(u"tbv_vars")
        self.tbv_vars.setSelectionMode(QAbstractItemView.NoSelection)

        self.horizontalLayout_5.addWidget(self.tbv_vars)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout.addWidget(self.widget_2)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 733, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"color: red")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"New Flow", None))
        self.lb_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.ln_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter name", None))
        self.lb_desc.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.pte_desc.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter description", None))
#if QT_CONFIG(tooltip)
        self.btn_edit_fluids.setToolTip(QCoreApplication.translate("MainWindow", u"add or remove working fluid", None))
#endif // QT_CONFIG(tooltip)
        self.btn_edit_fluids.setText(QCoreApplication.translate("MainWindow", u"Fluids", None))
        self.lb_fluids.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Variables with range defined will appear here", None))
        self.chb_auto_calc.setText(QCoreApplication.translate("MainWindow", u"Auto calculate on slider release", None))
        self.btn_calc.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
#if QT_CONFIG(tooltip)
        self.lb_flow.setToolTip(QCoreApplication.translate("MainWindow", u"Here you need to define variables and state points in order", None))
#endif // QT_CONFIG(tooltip)
        self.lb_flow.setText(QCoreApplication.translate("MainWindow", u"Calculation Logic & Flow:", None))
        self.btn_new_var.setText(QCoreApplication.translate("MainWindow", u"New Variable", None))
        self.btn_new_state.setText(QCoreApplication.translate("MainWindow", u"New State", None))
    # retranslateUi

