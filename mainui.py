# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QtCore.QSize(800, 600))
        Form.setMaximumSize(QtCore.QSize(800, 600))
        self.pushButtonSingle = QtWidgets.QPushButton(Form)
        self.pushButtonSingle.setGeometry(QtCore.QRect(270, 130, 231, 71))
        self.pushButtonSingle.setObjectName("pushButtonSingle")
        self.pushButtonNetwork = QtWidgets.QPushButton(Form)
        self.pushButtonNetwork.setGeometry(QtCore.QRect(270, 330, 231, 71))
        self.pushButtonNetwork.setObjectName("pushButtonNetwork")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setStyleSheet("background-image: url(./sources/mainbg.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.pushButtonNetwork.raise_()
        self.pushButtonSingle.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Reservi"))
        self.pushButtonSingle.setText(_translate("Form", "单人游戏"))
        self.pushButtonNetwork.setText(_translate("Form", "在线对战"))
