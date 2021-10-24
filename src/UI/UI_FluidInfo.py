from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(400, 280)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.hl_dialog = QHBoxLayout()
        self.hl_dialog.setObjectName(u"hl_dialog")
        self.lb_name = QLabel(Dialog)
        self.lb_name.setObjectName(u"lb_name")
        font = QFont()
        font.setPointSize(10)
        self.lb_name.setFont(font)
        self.lb_name.setAlignment(Qt.AlignCenter)

        self.hl_dialog.addWidget(self.lb_name)

        self.lb_formula = QLabel(Dialog)
        self.lb_formula.setObjectName(u"lb_formula")
        self.lb_formula.setAlignment(Qt.AlignCenter)

        self.hl_dialog.addWidget(self.lb_formula)


        self.verticalLayout.addLayout(self.hl_dialog)

        self.tbv_info = QTableView(Dialog)
        self.tbv_info.setObjectName(u"tbv_info")
        self.tbv_info.setFocusPolicy(Qt.NoFocus)
        self.tbv_info.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbv_info.setTabKeyNavigation(False)
        self.tbv_info.setProperty("showDropIndicator", False)
        self.tbv_info.setDragDropOverwriteMode(False)
        self.tbv_info.setSelectionMode(QAbstractItemView.NoSelection)

        self.verticalLayout.addWidget(self.tbv_info)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Fluid Info", None))
        self.lb_name.setText(QCoreApplication.translate("Dialog", u"Fluid Name", None))
        self.lb_formula.setText(QCoreApplication.translate("Dialog", u"Formula", None))
    # retranslateUi

