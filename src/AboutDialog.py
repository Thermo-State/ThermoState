from PySide2.QtGui import QMovie
from PySide2.QtWidgets import QDialog, QLayout
from UI.UI_AboutDialog import Ui_DialogAbout
from ProgramVariables import ProgramInfo
from UI import images_rc # noqa


class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_DialogAbout()
        self.ui.setupUi(self)

        movie = QMovie(':/anim/Resources/ts.gif')
        self.ui.lb_logo.setMovie(movie)
        movie.start()
        self.ui.lb_version.setText(ProgramInfo.name + " " + ProgramInfo.version)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
