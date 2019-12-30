from Base import *
from BaseUi import UiBaseForm
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget


class SinglePlayer(UiBaseForm, QWidget):
    """
    单人游戏
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._chessboard = ChessBoard()
        self._is_over = False
        self._current_color = 'b'

        self.buttonBack.clicked.connect(self._back)
        self.buttonGiveIn.clicked.connect(self._give_in)
        self.buttonRegret.clicked.connect(self._regret)
        self.buttonStart.clicked.connect(self._start)

    def _back(self):
        pass

    def _start(self):
        pass

    def _give_in(self):
        pass

    def _regret(self):
        pass

