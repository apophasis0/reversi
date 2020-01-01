from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QCloseEvent, QIcon, QBrush, QPixmap, QMouseEvent
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from typing import List, Set, Union, Tuple
import itertools

# 棋盘 左上角位于 (25px, 25px)
# 每格宽为 68px，边框宽 1px
# chessboard = [[None for i in range(8)] for j in range(8)]
PIVOT = (25, 25)
GRID_SIZE = 68
BORDER_SIZE = 1


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

    def legal_points(self, color: str) -> List:
        res = set()
        for i in range(8):
            for j in range(8):
                # 自身是空的
                if self.board[i][j] is None:
                    legal_flag: bool = False  # 已经确定这一格合法后，就直接判断下一格
                    # 对应相邻格子存在，且格子里有异色棋子，则进入分支
                    # 左上
                    if i - 1 >= 0 and j - 1 >= 0 and isinstance(self.board[i - 1][j - 1], Chessman) \
                            and self.board[i - 1][j - 1].color != color:
                        adjacent_color = self.board[i - 1][j - 1].color
                        m, n = i - 2, j - 2
                        while m >= 0 and n >= 0:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            m -= 1
                            n -= 1
                    # 上
                    if not legal_flag and i - 1 >= 0 and isinstance(self.board[i - 1][j], Chessman) \
                            and self.board[i - 1][j].color != color:
                        adjacent_color = self.board[i - 1][j].color
                        m, n = i - 2, j
                        while m >= 0:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            m -= 1
                    # 右上
                    if not legal_flag and i - 1 >= 0 and j + 1 < 8 and isinstance(self.board[i - 1][j + 1], Chessman) \
                            and self.board[i - 1][j + 1].color != color:
                        adjacent_color = self.board[i - 1][j + 1].color
                        m, n = i - 2, j + 2
                        while m >= 0 and n < 8:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            m -= 1
                            n += 1
                    # 左
                    if not legal_flag and j - 1 >= 0 and isinstance(self.board[i][j - 1], Chessman) and \
                            self.board[i][j - 1].color != color:
                        adjacent_color = self.board[i][j - 1]
                        m, n = i, j - 2
                        while n >= 0:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            n -= 1
                    # 右
                    if not legal_flag and j + 1 < 8 and isinstance(self.board[i][j + 1], Chessman) and \
                            self.board[i][j + 1].color != color:
                        adjacent_color = self.board[i][j + 1]
                        m, n = i, j + 2
                        while n < 8:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            n += 1
                    # 左下
                    if not legal_flag and i + 1 < 8 and j - 1 >= 0 and isinstance(self.board[i + 1][j - 1], Chessman) \
                            and self.board[i + 1][j - 1].color != color:
                        adjacent_color = self.board[i + 1][j - 1].color
                        m, n = i + 2, j - 2
                        while m < 8 and j >= 0:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            m += 1
                            n -= 1
                    # 下
                    if not legal_flag and i + 1 < 8 and isinstance(self.board[i + 1][j], Chessman) and \
                            self.board[i + 1][j].color != color:
                        adjacent_color = self.board[i + 1][j].color
                        m, n = i + 2, j
                        while m < 8:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            m += 1
                    # 右下
                    if not legal_flag and i + 1 < 8 and j + 1 < 8 and isinstance(self.board[i + 1][j + 1], Chessman) \
                            and self.board[i + 1][j + 1].color != color:
                        adjacent_color = self.board[i + 1][j + 1].color
                        m, n = i + 2, j + 2
                        while m < 8 and n < 8:
                            if isinstance(self.board[m][n], Chessman):
                                if self.board[m][n].color != adjacent_color:
                                    res.add((j, i))
                                    legal_flag = True
                                    break
                            else:
                                break
                            m += 1
                            n += 1
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
            '''
            更新棋盘
            '''
            # 列举出8个方向
            DIRECTIONS: List[Tuple] = [d for d in itertools.product((0, 1, -1), repeat=2) if d != (0, 0)]
            for d in DIRECTIONS:  # 遍历每个方向
                x, y = coord[0] + d[0], coord[1] + d[1]
                chess_on_line = list()  # 储存该方向上的所有棋子
                while 0 <= x < 8 and 0 <= y < 8 and self.board[y][x] is not None:  # 当前坐标位于棋盘内且有棋子
                    chess_on_line.append(self.board[y][x])
                    x, y = x + d[0], y + d[1]
                if chess_on_line != [] and chess_on_line[-1].color == chessman.color:
                    # 最后一个颜色的子与当前子同色表明这一方向需要翻面
                    for c in chess_on_line:
                        if c.color != chessman.color:
                            c.reverse()


def trans_position(a0: QMouseEvent) -> Tuple[int, int]:
    x = a0.x()
    y = a0.y()
    return (x - PIVOT[0]) // (BORDER_SIZE + GRID_SIZE), (y - PIVOT[1]) // (BORDER_SIZE + GRID_SIZE)


if __name__ == '__main__':
    pass
    # Unit Test
    # board = ChessBoard()
    # board.put_chessman(Chessman('w'), (3, 3))
    # board.put_chessman(Chessman('w'), (4, 4))
    # board.put_chessman(Chessman('b'), (4, 3))
    # board.put_chessman(Chessman('b'), (3, 4))
    # print(board.legal_points('b'))
