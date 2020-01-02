import cgitb
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget

from NetworkPlayer import NetworkConfig
from SinglePlayer import SinglePlayer
from mainui import Ui_Form

cgitb.enable(format='error')
app = None
ADDR = ("127.0.0.1", 12222)


class MainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButtonSingle.clicked.connect(self.single)
        self.pushButtonNetwork.clicked.connect(self.network)

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
