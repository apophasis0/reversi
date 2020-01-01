import cgitb

cgitb.enable(format='error')

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont

from SinglePlayer import SinglePlayer
from NetworkPlayer import NetworkConfig

app = None
ADDR = ("127.0.0.1", 10223)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        self.pushButtonSingle = QtWidgets.QPushButton(Form)
        self.pushButtonSingle.setGeometry(QtCore.QRect(200, 100, 231, 71))
        self.pushButtonSingle.setObjectName("pushButtonSingle")
        self.pushButtonSingle.clicked.connect(self.single)
        self.pushButtonNetwork = QtWidgets.QPushButton(Form)
        self.pushButtonNetwork.setGeometry(QtCore.QRect(200, 260, 231, 71))
        self.pushButtonNetwork.setObjectName("pushButtonNetwork")
        self.pushButtonNetwork.clicked.connect(self.network)

        self.gameWindow = None

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButtonSingle.setText(_translate("Form", "单人游戏"))
        self.pushButtonNetwork.setText(_translate("Form", "在线对战"))

    def single(self):
        self.close()
        self.gameWindow = SinglePlayer()
        self.gameWindow.exitSignal.connect(self.game_over)
        self.gameWindow.backSignal.connect(self.show)
        self.gameWindow.show()

    def network(self):
        self.close()
        self.gameWindow = NetworkConfig(main_win=self, addr=ADDR)
        self.gameWindow.show()

    def game_over(self):
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    font = QFont()
    font.setFamilies(["微软雅黑"])
    font.setPointSize(14)
    main_win.setFont(font)
    main_win.show()
    sys.exit(app.exec_())
