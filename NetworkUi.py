# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'network.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_FormNetwork(object):
    def setupUi(self, FormNetwork):
        FormNetwork.setObjectName("FormNetwork")
        FormNetwork.resize(300, 340)
        self.verticalLayoutWidget = QtWidgets.QWidget(FormNetwork)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelName = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        self.lineEditName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEditName.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEditName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listPlayers = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listPlayers.setObjectName("listPlayers")
        self.verticalLayout.addWidget(self.listPlayers)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonCreate = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButtonCreate.setObjectName("pushButtonCreate")
        self.horizontalLayout_2.addWidget(self.pushButtonCreate)
        self.pushButtonRefresh = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.horizontalLayout_2.addWidget(self.pushButtonRefresh)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(FormNetwork)
        QtCore.QMetaObject.connectSlotsByName(FormNetwork)

    def retranslateUi(self, FormNetwork):
        _translate = QtCore.QCoreApplication.translate
        FormNetwork.setWindowTitle(_translate("FormNetwork", "在线玩家"))
        self.labelName.setText(_translate("FormNetwork", "玩家名:"))
        self.pushButtonCreate.setText(_translate("FormNetwork", "创建游戏"))
        self.pushButtonRefresh.setText(_translate("FormNetwork", "刷新"))
