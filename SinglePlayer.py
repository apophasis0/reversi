import random

from PyQt5 import QtGui

from Base import *
from BaseUi import BaseWidget


class SinglePlayer(BaseWidget):
    """
    单人游戏
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._chessboard = ChessBoard()
        self._is_over = False
        self._current_color = 'b'

        self._chessboard.set_chessman(Chessman('w', self), (3, 3))
        self._chessboard.set_chessman(Chessman('w', self), (4, 4))
        self._chessboard.set_chessman(Chessman('b', self), (3, 4))
        self._chessboard.set_chessman(Chessman('b', self), (4, 3))

        self.buttonBack.clicked.connect(self.back)
        self.buttonGiveIn.clicked.connect(self._give_in)
        # self.buttonRegret.clicked.connect(self._regret)
        self.buttonStart.clicked.connect(self._start)
        self.win_label = None
        self.win_pic = None

        self._history = []

    def _start(self):
        if self.win_label is not None:
            self.win_label.hide()
        for i in range(8):
            for j in range(8):
                if self._chessboard.board[i][j] is not None:
                    self._chessboard.board[i][j].hide()
                    self._chessboard.board[i][j] = None
        self._chessboard = ChessBoard()
        self._is_over = False
        self._current_color = 'b'
        self._chessboard.set_chessman(Chessman('w', self), (3, 3))
        self._chessboard.set_chessman(Chessman('w', self), (4, 4))
        self._chessboard.set_chessman(Chessman('b', self), (3, 4))
        self._chessboard.set_chessman(Chessman('b', self), (4, 3))

        order = random.randint(0, 1)
        if order == 0:  # 如果为0后手
            self.auto_run()

    def _give_in(self):
        if not self._is_over:
            if self._current_color == 'b':
                self.win('w')
            else:
                self.win('b')

    def _regret(self):
        pass

    def win(self, color):
        """
        黑棋或白棋获胜
        """
        self.win_label = QLabel(self)
        if color == 'b':
            self.win_pic = QPixmap('./sources/black_win.png')
        elif color == 'w':
            self.win_pic = QPixmap('./sources/white_win.png')
        self.win_label.setPixmap(self.win_pic)
        self.win_label.resize(self.win_pic.size())
        self.win_label.move(50, 50)
        self.win_label.show()
        self._is_over = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self._is_over:
            return
        legal_points = self._chessboard.legal_points(self._current_color)
        if len(legal_points) == 0:
            self.change_color()
            self.auto_run()
            return
        if PIVOT[0] <= a0.x() <= PIVOT[0] + 8 * (GRID_SIZE + BORDER_SIZE) and \
                PIVOT[1] <= a0.y() <= PIVOT[1] + 8 * (GRID_SIZE + BORDER_SIZE):
            pos = trans_position(a0)
            # 位置不为空
            if self._chessboard.board[pos[1]][pos[0]] is not None:
                return

            # 为空
            if pos in legal_points:
                self._chessboard.put_chessman(Chessman(self._current_color, self), pos)
                self.change_color()

            winner = self._chessboard.is_finish()
            if winner is not None:
                self.win(winner)
            if pos in legal_points:
                self.auto_run()

    def change_color(self):
        if self._current_color == 'w':
            self._current_color = 'b'
        else:
            self._current_color = 'w'

    def auto_run(self):
        if self._is_over:
            return
        legal_points = self._chessboard.legal_points(self._current_color)
        if len(legal_points) == 0:
            return

        # 使用贪心策略，只迭代一步
        scores = list(map(lambda x: self._chessboard.fake_put_chessman(self._current_color, x), legal_points))
        i = scores.index(max(scores))
        self._chessboard.put_chessman(Chessman(self._current_color, self), legal_points[i])
        self.change_color()

        winner = self._chessboard.is_finish()
        if winner is not None:
            self.win(winner)
            return


if __name__ == '__main__':
    s = SinglePlayer()
    s._chessboard.legal_points('b')
