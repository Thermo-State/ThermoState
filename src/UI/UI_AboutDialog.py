from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import images_rc


class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        if not DialogAbout.objectName():
            DialogAbout.setObjectName(u"DialogAbout")
        DialogAbout.setWindowModality(Qt.WindowModal)
        DialogAbout.resize(536, 460)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogAbout.sizePolicy().hasHeightForWidth())
        DialogAbout.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/png/Resources/TS-bold.png", QSize(), QIcon.Normal, QIcon.Off)
        DialogAbout.setWindowIcon(icon)
        DialogAbout.setModal(True)
        self.verticalLayout = QVBoxLayout(DialogAbout)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(DialogAbout)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lb_logo = QLabel(self.widget)
        self.lb_logo.setObjectName(u"lb_logo")
        self.lb_logo.setMinimumSize(QSize(500, 220))
        self.lb_logo.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.lb_logo)

        self.lb_txt = QLabel(self.widget)
        self.lb_txt.setObjectName(u"lb_txt")
        self.lb_txt.setMinimumSize(QSize(0, 0))
        self.lb_txt.setFrameShape(QFrame.StyledPanel)
        self.lb_txt.setFrameShadow(QFrame.Plain)
        self.lb_txt.setTextFormat(Qt.RichText)
        self.lb_txt.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.lb_txt.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.lb_txt)

        self.lb_version = QLabel(self.widget)
        self.lb_version.setObjectName(u"lb_version")
        self.lb_version.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lb_version)

        self.verticalLayout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(DialogAbout)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogAbout)
        self.buttonBox.accepted.connect(DialogAbout.accept)
        self.buttonBox.rejected.connect(DialogAbout.reject)

        QMetaObject.connectSlotsByName(DialogAbout)

    # setupUi

    def retranslateUi(self, DialogAbout):
        DialogAbout.setWindowTitle(QCoreApplication.translate("DialogAbout", u"About", None))
        self.lb_logo.setText("")
        self.lb_txt.setText(QCoreApplication.translate("DialogAbout",
                                                       u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                       "p, li { white-space: pre-wrap; }\n"
                                                       "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">ThermoState wouldn't be possible without PySide2, CoolProp, PyqtGraph and Numpy</span></p>\n"
                                                       "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;\"><br /></p>\n"
                                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">If you have any suggesion or feedback, feel free to </sp"
                                                       "an><a href=\"2k4ieujtq@relay.firefox.com\"><span style=\" font-size:9pt; text-decoration: underline; color:#0000ff;\">email</span></a><span style=\" font-size:9pt;\"> me.</span></p>\n"
                                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">If you have any feature request or bug to report, open a github </span><a href=\"https://github.com/Thermo-State/ThermoState/issues\"><span style=\" font-size:9pt; text-decoration: underline; color:#0000ff;\">issue</span></a><span style=\" font-size:9pt;\">.</span></p>\n"
                                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\"> (Right click on the blue text to copy address)</span></p>\n"
                                                       "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; f"
                                                       "ont-size:9pt;\"><br /></p>\n"
                                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">The idea of ThernoState sprang from a project that I did with Bishal and Samin.</span></p>\n"
                                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">IUT MCE 17</span></p></body></html>",
                                                       None))
        self.lb_version.setText(QCoreApplication.translate("DialogAbout", u"ThermoState 1.0", None))
    # retranslateUi
