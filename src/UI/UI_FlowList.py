from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(420, 255)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_advanced_calc = QtWidgets.QLabel(Form)
        self.lb_advanced_calc.setObjectName("lb_advanced_calc")
        self.horizontalLayout.addWidget(self.lb_advanced_calc)
        self.btn_new_flow = QtWidgets.QPushButton(Form)
        self.btn_new_flow.setObjectName("btn_new_flow")
        self.horizontalLayout.addWidget(self.btn_new_flow)
        self.btn_delete_flow = QtWidgets.QPushButton(Form)
        self.btn_delete_flow.setObjectName("btn_delete_flow")
        self.horizontalLayout.addWidget(self.btn_delete_flow)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lv_flowList = QtWidgets.QListView(Form)
        self.lv_flowList.setObjectName("lv_flowList")
        self.verticalLayout.addWidget(self.lv_flowList)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lb_advanced_calc.setText(_translate("Form", "Advanced Calculation"))
        self.btn_new_flow.setText(_translate("Form", "Define new"))
        self.btn_delete_flow.setText(_translate("Form", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

