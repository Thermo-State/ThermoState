from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(307, 380)
        Dialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lb_stateNo = QLabel(Dialog)
        self.lb_stateNo.setObjectName(u"lb_stateNo")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_stateNo)

        self.lb_desc = QLabel(Dialog)
        self.lb_desc.setObjectName(u"lb_desc")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_desc)

        self.lb_fluid = QLabel(Dialog)
        self.lb_fluid.setObjectName(u"lb_fluid")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lb_fluid)

        self.cb_input_fluid = QComboBox(Dialog)
        self.cb_input_fluid.setObjectName(u"cb_input_fluid")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cb_input_fluid)

        self.lb_inp1 = QLabel(Dialog)
        self.lb_inp1.setObjectName(u"lb_inp1")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lb_inp1)

        self.wgt_inp1 = QWidget(Dialog)
        self.wgt_inp1.setObjectName(u"wgt_inp1")
        self.verticalLayout = QVBoxLayout(self.wgt_inp1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cb_input_1 = QComboBox(self.wgt_inp1)
        self.cb_input_1.setObjectName(u"cb_input_1")

        self.horizontalLayout.addWidget(self.cb_input_1)

        self.cb_unit_1 = QComboBox(self.wgt_inp1)
        self.cb_unit_1.setObjectName(u"cb_unit_1")

        self.horizontalLayout.addWidget(self.cb_unit_1)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.rb_indep1 = QRadioButton(self.wgt_inp1)
        self.rb_indep1.setObjectName(u"rb_indep1")
        self.rb_indep1.setChecked(True)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.rb_indep1)

        self.dspin_1 = QDoubleSpinBox(self.wgt_inp1)
        self.dspin_1.setObjectName(u"dspin_1")
        self.dspin_1.setDecimals(5)
        self.dspin_1.setMinimum(-10000000.000000000000000)
        self.dspin_1.setMaximum(99990000.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.dspin_1)

        self.rb_dep1 = QRadioButton(self.wgt_inp1)
        self.rb_dep1.setObjectName(u"rb_dep1")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.rb_dep1)

        self.cb_dep_var_1 = QComboBox(self.wgt_inp1)
        self.cb_dep_var_1.setObjectName(u"cb_dep_var_1")
        self.cb_dep_var_1.setEnabled(False)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.cb_dep_var_1)


        self.verticalLayout.addLayout(self.formLayout_2)


        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.wgt_inp1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label)

        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cb_input_2 = QComboBox(self.widget)
        self.cb_input_2.setObjectName(u"cb_input_2")

        self.horizontalLayout_2.addWidget(self.cb_input_2)

        self.cb_unit_2 = QComboBox(self.widget)
        self.cb_unit_2.setObjectName(u"cb_unit_2")

        self.horizontalLayout_2.addWidget(self.cb_unit_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.rb_indep2 = QRadioButton(self.widget)
        self.rb_indep2.setObjectName(u"rb_indep2")
        self.rb_indep2.setChecked(True)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.rb_indep2)

        self.dspin_2 = QDoubleSpinBox(self.widget)
        self.dspin_2.setObjectName(u"dspin_2")
        self.dspin_2.setDecimals(5)
        self.dspin_2.setMinimum(-10000000.000000000000000)
        self.dspin_2.setMaximum(99990000.000000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.dspin_2)

        self.rb_dep2 = QRadioButton(self.widget)
        self.rb_dep2.setObjectName(u"rb_dep2")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.rb_dep2)

        self.cb_dep_var_2 = QComboBox(self.widget)
        self.cb_dep_var_2.setObjectName(u"cb_dep_var_2")
        self.cb_dep_var_2.setEnabled(False)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.cb_dep_var_2)


        self.verticalLayout_3.addLayout(self.formLayout_3)


        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.widget)

        self.pte_desc = QPlainTextEdit(Dialog)
        self.pte_desc.setObjectName(u"pte_desc")
        self.pte_desc.setMaximumSize(QSize(16777215, 60))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pte_desc)

        self.spin_stateNo = QSpinBox(Dialog)
        self.spin_stateNo.setObjectName(u"spin_stateNo")
        self.spin_stateNo.setMinimum(1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spin_stateNo)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.lb_error = QLabel(Dialog)
        self.lb_error.setObjectName(u"lb_error")
        self.lb_error.setStyleSheet(u"color: red")
        self.lb_error.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.lb_error)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.rb_dep1.toggled.connect(self.cb_dep_var_1.setEnabled)
        self.rb_dep1.toggled.connect(self.dspin_1.setDisabled)
        self.rb_indep1.toggled.connect(self.cb_dep_var_1.setDisabled)
        self.rb_indep1.toggled.connect(self.dspin_1.setEnabled)
        self.rb_dep2.toggled.connect(self.cb_dep_var_2.setEnabled)
        self.rb_dep2.toggled.connect(self.dspin_2.setDisabled)
        self.rb_indep2.toggled.connect(self.dspin_2.setEnabled)
        self.rb_indep2.toggled.connect(self.cb_dep_var_2.setDisabled)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New State", None))
        self.lb_stateNo.setText(QCoreApplication.translate("Dialog", u"State No", None))
        self.lb_desc.setText(QCoreApplication.translate("Dialog", u"Description", None))
        self.lb_fluid.setText(QCoreApplication.translate("Dialog", u"Fluid", None))
        self.lb_inp1.setText(QCoreApplication.translate("Dialog", u"Input 1", None))
        self.rb_indep1.setText(QCoreApplication.translate("Dialog", u"Independent", None))
        self.rb_dep1.setText(QCoreApplication.translate("Dialog", u"Dependent", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Input 2", None))
        self.rb_indep2.setText(QCoreApplication.translate("Dialog", u"Independent", None))
        self.rb_dep2.setText(QCoreApplication.translate("Dialog", u"Dependent", None))
        self.pte_desc.setPlaceholderText(QCoreApplication.translate("Dialog", u"[Optional] write short description", None))
        self.lb_error.setText("")
    # retranslateUi

