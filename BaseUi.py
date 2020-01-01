# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basewidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget


class UiBaseForm(object):
    """
    由 pyguic 生成
    """
    def setupUi(self, BaseForm):
        BaseForm.setObjectName("BaseForm")
        BaseForm.resize(800, 600)
        BaseForm.setMinimumSize(QtCore.QSize(800, 600))
        BaseForm.setMaximumSize(QtCore.QSize(800, 600))
        BaseForm.setStyleSheet("")
        self.buttonStart = QtWidgets.QPushButton(BaseForm)
        self.buttonStart.setGeometry(QtCore.QRect(680, 160, 91, 31))
        self.buttonStart.setObjectName("buttonStart")
        self.buttonRegret = QtWidgets.QPushButton(BaseForm)
        self.buttonRegret.setGeometry(QtCore.QRect(680, 210, 91, 31))
        self.buttonRegret.setObjectName("buttonRegret")
        self.buttonGiveIn = QtWidgets.QPushButton(BaseForm)
        self.buttonGiveIn.setGeometry(QtCore.QRect(680, 260, 91, 31))
        self.buttonGiveIn.setObjectName("buttonGiveIn")
        self.buttonBack = QtWidgets.QPushButton(BaseForm)
        self.buttonBack.setGeometry(QtCore.QRect(680, 20, 91, 31))
        self.buttonBack.setObjectName("buttonBack")
        self.labelRemainingTime = QtWidgets.QLabel(BaseForm)
        self.labelRemainingTime.setGeometry(QtCore.QRect(680, 320, 91, 31))
        self.labelRemainingTime.setText("")
        self.labelRemainingTime.setObjectName("labelRemainingTime")
        self.frame = QtWidgets.QFrame(BaseForm)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frame.setStyleSheet("background-image: url(./sources/background2.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.buttonStart.raise_()
        self.buttonRegret.raise_()
        self.buttonGiveIn.raise_()
        self.buttonBack.raise_()
        self.labelRemainingTime.raise_()

        self.retranslateUi(BaseForm)
        QtCore.QMetaObject.connectSlotsByName(BaseForm)

    def retranslateUi(self, BaseForm):
        _translate = QtCore.QCoreApplication.translate
        BaseForm.setWindowTitle(_translate("BaseForm", "Form"))
        self.buttonStart.setText(_translate("BaseForm", "开始"))
        self.buttonRegret.setText(_translate("BaseForm", "悔棋"))
        self.buttonGiveIn.setText(_translate("BaseForm", "认输"))
        self.buttonBack.setText(_translate("BaseForm", "返回"))


class BaseWidget(QWidget, UiBaseForm):
    """
    窗口基类
    """
    backSignal = pyqtSignal()
    exitSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.is_exit = True

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.is_exit:
            self.exitSignal.emit()
        else:
            self.backSignal.emit()

    def back(self):
        self.is_exit = False
        self.close()

    def logo_move(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = BaseWidget()
    mainwin.show()
    sys.exit(app.exec_())
