from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(573, 403)
        Dialog.setModal(True)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lb_name = QLabel(self.widget)
        self.lb_name.setObjectName(u"lb_name")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_name)

        self.ln_name = QLineEdit(self.widget)
        self.ln_name.setObjectName(u"ln_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ln_name)

        self.lb_desc = QLabel(self.widget)
        self.lb_desc.setObjectName(u"lb_desc")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_desc)

        self.pte_desc = QPlainTextEdit(self.widget)
        self.pte_desc.setObjectName(u"pte_desc")
        self.pte_desc.setMaximumSize(QSize(16777215, 80))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pte_desc)

        self.lb_type = QLabel(self.widget)
        self.lb_type.setObjectName(u"lb_type")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lb_type)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rb_indep = QRadioButton(self.widget_3)
        self.rb_indep.setObjectName(u"rb_indep")
        self.rb_indep.setChecked(True)

        self.verticalLayout.addWidget(self.rb_indep)

        self.rb_dep = QRadioButton(self.widget_3)
        self.rb_dep.setObjectName(u"rb_dep")

        self.verticalLayout.addWidget(self.rb_dep)


        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.widget_3)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.lb_error = QLabel(self.widget)
        self.lb_error.setObjectName(u"lb_error")
        self.lb_error.setStyleSheet(u"color: red")
        self.lb_error.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.lb_error)


        self.horizontalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(Dialog)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stwgt_input = QStackedWidget(self.widget_2)
        self.stwgt_input.setObjectName(u"stwgt_input")
        self.pg_indep = QWidget()
        self.pg_indep.setObjectName(u"pg_indep")
        self.verticalLayout_5 = QVBoxLayout(self.pg_indep)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lb_enter_value = QLabel(self.pg_indep)
        self.lb_enter_value.setObjectName(u"lb_enter_value")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lb_enter_value)

        self.dspin_value = QDoubleSpinBox(self.pg_indep)
        self.dspin_value.setObjectName(u"dspin_value")
        self.dspin_value.setDecimals(5)
        self.dspin_value.setMinimum(-10000000.000000000000000)
        self.dspin_value.setMaximum(99990000.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.dspin_value)


        self.verticalLayout_5.addLayout(self.formLayout_2)

        self.wgt_rng = QWidget(self.pg_indep)
        self.wgt_rng.setObjectName(u"wgt_rng")
        self.verticalLayout_9 = QVBoxLayout(self.wgt_rng)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.chb_range = QCheckBox(self.wgt_rng)
        self.chb_range.setObjectName(u"chb_range")

        self.verticalLayout_9.addWidget(self.chb_range)

        self.wgt_range = QWidget(self.wgt_rng)
        self.wgt_range.setObjectName(u"wgt_range")
        self.wgt_range.setEnabled(False)
        self.horizontalLayout_2 = QHBoxLayout(self.wgt_range)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.dspin_r1 = QDoubleSpinBox(self.wgt_range)
        self.dspin_r1.setObjectName(u"dspin_r1")
        self.dspin_r1.setMinimum(-10000000.000000000000000)
        self.dspin_r1.setMaximum(99990000.000000000000000)

        self.horizontalLayout_2.addWidget(self.dspin_r1)

        self.label_4 = QLabel(self.wgt_range)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.dspin_r2 = QDoubleSpinBox(self.wgt_range)
        self.dspin_r2.setObjectName(u"dspin_r2")
        self.dspin_r2.setMinimum(-10000000.000000000000000)
        self.dspin_r2.setMaximum(99990000.000000000000000)

        self.horizontalLayout_2.addWidget(self.dspin_r2)

        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 3)

        self.verticalLayout_9.addWidget(self.wgt_range)

        self.lb_rng_details = QLabel(self.wgt_rng)
        self.lb_rng_details.setObjectName(u"lb_rng_details")
        self.lb_rng_details.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.lb_rng_details)


        self.verticalLayout_5.addWidget(self.wgt_rng)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.stwgt_input.addWidget(self.pg_indep)
        self.pg_dep = QWidget()
        self.pg_dep.setObjectName(u"pg_dep")
        self.verticalLayout_6 = QVBoxLayout(self.pg_dep)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.rb_state = QRadioButton(self.pg_dep)
        self.rb_state.setObjectName(u"rb_state")
        self.rb_state.setChecked(True)

        self.verticalLayout_6.addWidget(self.rb_state)

        self.wgt_state = QWidget(self.pg_dep)
        self.wgt_state.setObjectName(u"wgt_state")
        self.verticalLayout_7 = QVBoxLayout(self.wgt_state)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.lb_state = QLabel(self.wgt_state)
        self.lb_state.setObjectName(u"lb_state")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.lb_state)

        self.cb_state = QComboBox(self.wgt_state)
        self.cb_state.setObjectName(u"cb_state")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.cb_state)

        self.lb_property = QLabel(self.wgt_state)
        self.lb_property.setObjectName(u"lb_property")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.lb_property)

        self.cb_property = QComboBox(self.wgt_state)
        self.cb_property.setObjectName(u"cb_property")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.cb_property)

        self.lb_unit = QLabel(self.wgt_state)
        self.lb_unit.setObjectName(u"lb_unit")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.lb_unit)

        self.cb_unit = QComboBox(self.wgt_state)
        self.cb_unit.setObjectName(u"cb_unit")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.cb_unit)


        self.verticalLayout_7.addLayout(self.formLayout_3)


        self.verticalLayout_6.addWidget(self.wgt_state)

        self.rb_expr = QRadioButton(self.pg_dep)
        self.rb_expr.setObjectName(u"rb_expr")

        self.verticalLayout_6.addWidget(self.rb_expr)

        self.wgt_expr = QWidget(self.pg_dep)
        self.wgt_expr.setObjectName(u"wgt_expr")
        self.wgt_expr.setEnabled(False)
        self.verticalLayout_8 = QVBoxLayout(self.wgt_expr)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lb_dependency = QLabel(self.wgt_expr)
        self.lb_dependency.setObjectName(u"lb_dependency")

        self.horizontalLayout_3.addWidget(self.lb_dependency)

        self.btn_add_inner = QPushButton(self.wgt_expr)
        self.btn_add_inner.setObjectName(u"btn_add_inner")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_inner.sizePolicy().hasHeightForWidth())
        self.btn_add_inner.setSizePolicy(sizePolicy)
        self.btn_add_inner.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_3.addWidget(self.btn_add_inner)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.tbv_inner = QTableView(self.wgt_expr)
        self.tbv_inner.setObjectName(u"tbv_inner")
        self.tbv_inner.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbv_inner.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbv_inner.horizontalHeader().setVisible(False)
        self.tbv_inner.horizontalHeader().setStretchLastSection(True)
        self.tbv_inner.verticalHeader().setVisible(False)

        self.verticalLayout_8.addWidget(self.tbv_inner)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lb_expression = QLabel(self.wgt_expr)
        self.lb_expression.setObjectName(u"lb_expression")

        self.horizontalLayout_4.addWidget(self.lb_expression)

        self.btn_expr_edit = QPushButton(self.wgt_expr)
        self.btn_expr_edit.setObjectName(u"btn_expr_edit")

        self.horizontalLayout_4.addWidget(self.btn_expr_edit)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.lb_expr = QLabel(self.wgt_expr)
        self.lb_expr.setObjectName(u"lb_expr")

        self.verticalLayout_8.addWidget(self.lb_expr)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)


        self.verticalLayout_6.addWidget(self.wgt_expr)

        self.stwgt_input.addWidget(self.pg_dep)

        self.verticalLayout_3.addWidget(self.stwgt_input)

        self.buttonBox = QDialogButtonBox(self.widget_2)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout.addWidget(self.widget_2)


        self.retranslateUi(Dialog)
        self.rb_expr.toggled.connect(self.wgt_expr.setEnabled)
        self.rb_expr.toggled.connect(self.wgt_state.setDisabled)
        self.rb_state.toggled.connect(self.wgt_expr.setDisabled)
        self.rb_state.toggled.connect(self.wgt_state.setEnabled)

        self.stwgt_input.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Variable", None))
        self.lb_name.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.ln_name.setText("")
        self.ln_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"Name w/o space", None))
        self.lb_desc.setText(QCoreApplication.translate("Dialog", u"Description", None))
        self.pte_desc.setPlaceholderText(QCoreApplication.translate("Dialog", u"[Optional] short Description", None))
        self.lb_type.setText(QCoreApplication.translate("Dialog", u"Variable Type", None))
        self.rb_indep.setText(QCoreApplication.translate("Dialog", u"Independent", None))
        self.rb_dep.setText(QCoreApplication.translate("Dialog", u"Dependent", None))
        self.lb_error.setText("")
        self.lb_enter_value.setText(QCoreApplication.translate("Dialog", u"Enter Value:", None))
        self.chb_range.setText(QCoreApplication.translate("Dialog", u"Range", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.lb_rng_details.setText(QCoreApplication.translate("Dialog", u"Setting range will allow you to change value with slider. Useful if you want to observe the effect of this variable on final calculation", None))
        self.rb_state.setText(QCoreApplication.translate("Dialog", u"Value from state point", None))
        self.lb_state.setText(QCoreApplication.translate("Dialog", u"Sate", None))
        self.lb_property.setText(QCoreApplication.translate("Dialog", u"Property", None))
        self.lb_unit.setText(QCoreApplication.translate("Dialog", u"Unit", None))
        self.rb_expr.setText(QCoreApplication.translate("Dialog", u"Value from expression", None))
        self.lb_dependency.setText(QCoreApplication.translate("Dialog", u"Inner Variable:", None))
        self.btn_add_inner.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.lb_expression.setText(QCoreApplication.translate("Dialog", u"Expression:", None))
        self.btn_expr_edit.setText(QCoreApplication.translate("Dialog", u"Edit", None))
        self.lb_expr.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi

