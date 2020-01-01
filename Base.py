import itertools
from typing import List, Union, Tuple

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QLabel

# 棋盘 左上角位于 (25px, 25px)
# 每格宽为 68px，边框宽 1px
# chessboard = [[None for i in range(8)] for j in range(8)]
PIVOT = (25, 25)
GRID_SIZE = 68
BORDER_SIZE = 1

# 列举出8个方向
DIRECTIONS: List[Tuple] = [d for d in itertools.product((0, 1, -1), repeat=2) if d != (0, 0)]


class Chessman(QLabel):
    """
    棋子类
    """

    def __init__(self, color: str, parent=None):
        assert color == 'w' or color == 'b'
        super().__init__(parent=parent)
        self.color = color
        self.pic = None
        if color == 'w':
            self.pic = QPixmap("./sources/white.png")
        else:
            self.pic = QPixmap("./sources/black.png")
        self.setFixedSize(self.pic.size())
        self.setPixmap(self.pic)

    def move_chessman(self, board, coord: QtCore.QPoint):
        x, y = coord.x(), coord.y()
        x0 = (x - PIVOT[0]) // (BORDER_SIZE + GRID_SIZE)
        y0 = (y - PIVOT[1]) // (BORDER_SIZE + GRID_SIZE)
        if x0 < 8 and y0 < 8:
            pic_x = PIVOT[0] + x0 * (BORDER_SIZE + GRID_SIZE) + BORDER_SIZE
            pic_y = PIVOT[1] + y0 * (BORDER_SIZE + GRID_SIZE) + BORDER_SIZE
            super().move(pic_x, pic_y)
            board.board[y0][x0] = self

    def reverse(self):
        self.color = 'w' if self.color == 'b' else 'b'
        if self.color == 'w':
            self.pic = QPixmap("./sources/white.png")
        else:
            self.pic = QPixmap("./sources/black.png")
        self.setPixmap(self.pic)


class ChessBoard(object):
    def __init__(self):
        self.board: List[List[Union[Chessman, None]]] = [[None for i in range(8)] for j in range(8)]
        self.empty_points = 64
        self.white_count = 0
        self.black_count = 0

    def is_finish(self) -> Union[None, str]:
        return None if self.empty_points > 0 else 'w' if self.white_count >= self.black_count else 'b'

    def legal_points(self, color: str) -> List[Union[None, Tuple[int, int]]]:
        res = set()
        for i in range(8):
            for j in range(8):
                # 自身是空的
                legal_flag = False
                if self.board[i][j] is None:
                    for d in DIRECTIONS:
                        m, n = i + d[0], j + d[1]  # 相邻格子
                        if 0 <= m < 8 and 0 <= n < 8 and self.board[m][n] is not None and \
                                self.board[m][n].color != color:  # 如果相邻格子异色
                            # 沿着个方向遍历
                            m, n = m + d[0], n + d[1]
                            while 0 <= m < 8 and 0 <= n < 8 and self.board[m][n] is not None:
                                # 如果这个当前格子有棋子
                                if self.board[m][n].color == color:
                                    # 并且遇到同色子，证明空格合法
                                    legal_flag = True
                                    break
                                m, n = m + d[0], n + d[1]
                        if legal_flag:
                            break
                if legal_flag:
                    res.add((j, i))
        print(res)
        return list(res)

    def set_chessman(self, chessman: Chessman, coord: Tuple[int, int]):
        """
        直接放置棋子，而不检查合法性，也不更新棋盘其他子的状态
        """
        self.board[coord[1]][coord[0]] = chessman
        self.empty_points -= 1
        chessman.move(PIVOT[0] + coord[0] * (BORDER_SIZE + GRID_SIZE),
                      PIVOT[1] + coord[1] * (BORDER_SIZE + GRID_SIZE))
        chessman.resize(GRID_SIZE, GRID_SIZE)
        chessman.show()

    def put_chessman(self, chessman: Chessman, coord: Tuple[int, int]):
        """
        正常落子
        """
        legal_points = self.legal_points(chessman.color)
        if coord in legal_points:
            self.board[coord[1]][coord[0]] = chessman
            chessman.move(PIVOT[0] + coord[0] * (BORDER_SIZE + GRID_SIZE),
                          PIVOT[1] + coord[1] * (BORDER_SIZE + GRID_SIZE))
            chessman.resize(GRID_SIZE, GRID_SIZE)
            chessman.show()
            self.empty_points -= 1

            # 更新棋盘
            for d in DIRECTIONS:  # 遍历每个方向
                x, y = coord[0] + d[0], coord[1] + d[1]
                chess_on_line = list()  # 储存该方向上的所有棋子
                flag = False
                while 0 <= x < 8 and 0 <= y < 8 and self.board[y][x] is not None:  # 当前坐标位于棋盘内且有棋子
                    if self.board[y][x].color != chessman.color:
                        chess_on_line.append(self.board[y][x])
                    elif self.board[y][x].color == chessman.color and len(chess_on_line) != 0:
                        flag = True
                        break
                    else:
                        break
                    x, y = x + d[0], y + d[1]
                if flag:
                    for c in chess_on_line:
                        if c.color != chessman.color:
                            c.reverse()


def trans_position(a0: QMouseEvent) -> Tuple[int, int]:
    x = a0.x()
    y = a0.y()
    return (x - PIVOT[0]) // (BORDER_SIZE + GRID_SIZE), (y - PIVOT[1]) // (BORDER_SIZE + GRID_SIZE)
