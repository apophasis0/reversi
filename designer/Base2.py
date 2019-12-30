# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basewidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QtCore.QSize(800, 600))
        Form.setMaximumSize(QtCore.QSize(800, 600))
        Form.setStyleSheet("")
        self.buttonStart = QtWidgets.QPushButton(Form)
        self.buttonStart.setGeometry(QtCore.QRect(680, 160, 91, 31))
        self.buttonStart.setObjectName("buttonStart")
        self.buttonRegret = QtWidgets.QPushButton(Form)
        self.buttonRegret.setGeometry(QtCore.QRect(680, 210, 91, 31))
        self.buttonRegret.setObjectName("buttonRegret")
        self.buttonGiveIn = QtWidgets.QPushButton(Form)
        self.buttonGiveIn.setGeometry(QtCore.QRect(680, 260, 91, 31))
        self.buttonGiveIn.setObjectName("buttonGiveIn")
        self.buttonBack = QtWidgets.QPushButton(Form)
        self.buttonBack.setGeometry(QtCore.QRect(680, 20, 91, 31))
        self.buttonBack.setObjectName("buttonBack")
        self.labelRemainingTime = QtWidgets.QLabel(Form)
        self.labelRemainingTime.setGeometry(QtCore.QRect(680, 320, 91, 31))
        self.labelRemainingTime.setObjectName("labelRemainingTime")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.frame.setStyleSheet("background-image: url(./sources/background.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.raise_()
        self.buttonStart.raise_()
        self.buttonRegret.raise_()
        self.buttonGiveIn.raise_()
        self.buttonBack.raise_()
        self.labelRemainingTime.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.buttonStart.setText(_translate("Form", "开始"))
        self.buttonRegret.setText(_translate("Form", "悔棋"))
        self.buttonGiveIn.setText(_translate("Form", "认输"))
        self.buttonBack.setText(_translate("Form", "返回"))
        self.labelRemainingTime.setText(_translate("Form", "TextLabel"))


class MainWin(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = MainWin()
    mainwin.show()
    sys.exit(app.exec_())

