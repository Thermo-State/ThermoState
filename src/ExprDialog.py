from functools import partial
from typing import Union, Dict, List

from PySide2 import QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QDialog, QPushButton, QLayout

from Model.VarState import Variable, MATH_FUNC_NAMES, ExprManager
from UI.UI_Expr import Ui_Dialog

id_to_key: Dict[str, str] = {"**": "^", "DEL": "backspace", "AC": "home"}


def getShortcutKey(bid: str):
    if bid in id_to_key:
        return id_to_key[bid]
    else:
        return bid


class ExprDialog(QDialog):
    expr_created: Signal = Signal(list, str)

    def __init__(self, parent, expr: List[Union[str, Variable]], ups_vars: List[Variable]):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ups_vars: List[Variable] = ups_vars
        self.ups_vars_name: List[str] = []
        self.ups_vars_ids: List[str] = []
        for v in self.ups_vars:
            self.ups_vars_name.append(v.name)
            self.ups_vars_ids.append(v.getIdentifier())

        self.ups_buttons: Dict[str, QPushButton] = {}

        self.expr_man = ExprManager(expr=expr, ups_vars=ups_vars)

        self.updateDisplay()

        self.id_num_btn: List[str] = ['7', '8', '9', 'DEL', 'AC', '4', '5', '6', '*', '/', '1', '2', '3', '+', '-',
                                      '0', '.', '**', '(', ')']

        self.num_buttons: Dict[str, QPushButton] = {}
        for i, bi in enumerate(self.id_num_btn):
            bl = ExprManager.getButtonLabel(bi)
            btn = QPushButton(bl)
            # noinspection PyTypeChecker
            btn.clicked.connect(partial(self.on_btn, bi))
            btn.setShortcut(getShortcutKey(bi))
            btn.setFixedSize(50, 50)
            self.num_buttons[bi] = btn

        for bi in ["DEL", "AC"]:
            self.num_buttons[bi].setStyleSheet("background-color: #DAF7A6; border: 1px solid black")

        row, col = 4, 5
        for i in range(row):
            for j in range(col):
                n = i * col + j
                bi = self.id_num_btn[n]
                self.ui.gl_nums.addWidget(self.num_buttons[bi], i, j)

        self.id_fun_btn: List[str] = MATH_FUNC_NAMES

        self.fun_buttons: Dict[str, QPushButton] = {}
        for i, bi in enumerate(self.id_fun_btn):
            bl = bi
            btn = QPushButton(bl)
            btn.clicked.connect(partial(self.on_btn, bi))
            btn.setFixedSize(50, 30)
            self.fun_buttons[bi] = btn
            self.ui.gl_funs.addWidget(btn, 0, i)

        if self.ups_vars:
            self.setup_ups_vars_btns()
        else:
            self.ui.sa_vars.hide()

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.on_ok_btn)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def setup_ups_vars_btns(self):
        col = 4
        i, j = 0, 0
        bw, bh = 50, 30
        for v in self.ups_vars:
            bl = v.name
            bi = v.getIdentifier()
            btn = QPushButton(bl)
            # noinspection PyTypeChecker
            btn.clicked.connect(partial(self.on_btn_var, v))
            btn.setFixedSize(bw, bh)
            self.ups_buttons[bi] = btn
            self.ui.gl_vars.addWidget(btn, i, j)
            if not j == col - 1:
                j = j + 1
            else:
                j = 0
                i = i + 1

        pw, ph = 15, 20
        if i == 0 or (i == 1 and j == 0):
            sw = (bw + pw) * col
            sh = (bh + ph)
        else:
            sw = (bw + pw) * col
            sh = (bh + ph) * 2

        self.ui.sa_vars.setMinimumWidth(sw)
        self.ui.sa_vars.setFixedHeight(sh)

    def on_btn(self, bi: str) -> None:
        if bi == "DEL":
            self.expr_man.pop()
        elif bi == "AC":
            self.expr_man.clear()
        else:
            self.expr_man.add(bi)

        self.updateDisplay()
        if bi in self.id_fun_btn:
            self.num_buttons["("].click()

    def on_btn_var(self, v: Variable) -> None:
        self.expr_man.add(v)
        self.updateDisplay()

    def updateDisplay(self):
        self.ui.lb_display.setText(self.expr_man.displayText())

    def on_ok_btn(self):
        if not self.validateExpDis():
            return

        self.expr_created.emit(self.expr_man.getExpr(), self.expr_man.displayText())
        self.close()

    def validateExpDis(self) -> bool:
        e = self.expr_man.displayText()
        len_e = len(e)
        last = len_e - 1
        count_lb = 0
        count_rb = 0
        for i, t in enumerate(e):
            if t == '(':
                count_lb = count_lb + 1
            elif t == ')':
                count_rb = count_rb + 1
            elif t in self.id_fun_btn:
                if not i == 0:
                    if e[i - 1] in "1234567890)" or e[i - 1] in self.ups_vars_name:
                        self.setErr("You must explicit type multiplication operator")
                        return False
                if i == last or not e[i + 1] == "(":
                    self.setErr("functions must be followed by brackets")
                    return False
                if not i == last - 1:
                    if e[i + 2] == ")":
                        self.setErr("function parameter can not be empty")
                        return False
            elif t in self.ups_vars_name:
                if not i == 0:
                    if e[i - 1] in "1234567890)" or e[i - 1] in self.ups_vars_name:
                        self.setErr("You must explicit type multiplication operator")
                        return False
                if not i == last:
                    if e[i + 1] in "(1234567890" or e[i + 1] in self.ups_vars_name:
                        self.setErr("You must explicit type multiplication operator")
                        return False
            elif t in "^×/+-":
                if i == last:
                    self.setErr("Invalid syntax")
                    return False
                elif i == 0 and t in "^×/":
                    self.setErr("Invalid syntax")
                    return False
            elif t == ".":
                if i == last or e[i + 1] not in "1234567890":
                    self.setErr("invalid decimal point")
                    return False

        if not count_lb == count_rb:
            self.setErr("You must close all bracket")
            return False
        return True

    def setErr(self, e: str):
        self.ui.lb_error.setText(e)
