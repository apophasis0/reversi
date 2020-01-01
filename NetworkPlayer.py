from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

from Base import *
from BaseUi import *
from NetworkUi import Ui_FormNetwork
from reversi_server.Player import *

receive_sock = Player.receive_sock


class NetworkConfig(QWidget, Ui_FormNetwork):
    """
    配置网络
    """
    dataSignal = pyqtSignal(dict, name='data')
    disconnectionSignal = pyqtSignal()

    def __init__(self, addr, main_win, parent=None):
        super().__init__(parent)

        self.main_win = main_win
        self.game_win = None
        self.is_create = False
        self.keep_recv = True
        self.addr = addr
        self.item = None

        # 网络连接
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(addr)
            self.is_connect = True
            Thread(target=self.recv_data).start()
            self.dataSignal.connect(self.deal_data)
        except ConnectionRefusedError as e:
            QMessageBox.information(self, "错误", "服务器连接失败")
            raise e

        self.setupUi(self)
        self.pushButtonRefresh.clicked.connect(self.refresh)
        self.refresh()
        self.listPlayers.itemDoubleClicked.connect(self.item_double_clicked)
        self.pushButtonJoin.clicked.connect(self.join_battle)
        self.pushButtonCreate.clicked.connect(self.create_game)
        self.disconnectionSignal.connect(self.disconnect_)

    @staticmethod
    def send_obj(sock: socket.socket, data: Dict[str, Any]):
        str_data: str = json.dumps(data) + " " + END_FLAG
        sock.sendall(str_data.encode())

    def refresh(self):
        data = {
            "target": "server",
            "message": "refresh",
            "data": ""
        }
        NetworkConfig.send_obj(self.sock, data)

    def disconnect_(self) -> None:
        QMessageBox.information(self, "消息", "连接断开，返回主界面")
        self.is_connect = False
        self.close()

    def recv_data(self):
        while self.keep_recv:
            try:
                recv = receive_sock(self.sock)
            except (ConnectionAbortedError, ConnectionResetError):
                self.disconnectionSignal.emit()
                break
            try:
                json_data = json.loads(recv)
                self.dataSignal.emit(json_data)
            except json.JSONDecodeError:
                logging.exception("解析错误: " + recv)

    def deal_data(self, json_data: Dict[str, Any]):
        if json_data["message"] == "player_list":
            self.listPlayers.clear()
            for name in json_data['data']:
                self.item = QListWidgetItem(name, self.listPlayers)
                self.listPlayers.addItem(self.item)
        elif json_data["message"] == "get_name":
            self.lineEditName.setText(json_data["data"])
        elif json_data["message"] == "reply":
            if json_data["type"] == "create":
                QMessageBox.information(self, "消息", json_data["data"])
                self.pushButtonJoin.setEnabled(False)
                self.lineEditName.setEnabled(True)
                self.is_create = False
                self.pushButtonCreate.setText("创建游戏")
            if json_data["type"] == "battle":
                if json_data["data"]:
                    self.game_win = NetworkPlayer(sock=self.sock, name=json_data["name"])
                    self.game_win.backSignal.connect(self.main_win.show)
                    self.game_win.exitSignal.connect(self.main_win.game_over)
                    self.game_win.show()
                    self.close()
                else:
                    QMessageBox.information(self, "消息", json_data["info"])

    def item_double_clicked(self, item):
        if not self.is_create:
            return
        data = {
            "target": "server",
            "message": "battle",
            "data": item.text()
        }
        NetworkConfig.send_obj(self.sock, data)

    def join_battle(self):
        """
        加入对战
        """
        data = {
            "target": "server",
            "message": "battle",
            "data": self.listPlayers.currentItem().text()
        }
        NetworkConfig.send_obj(self.sock, data)

    def create_game(self):
        """
        创建游戏
        """
        if not self.is_create:
            data = {
                "target": "server",
                "message": "create",
                "data": self.lineEditName.text().strip()
            }
            NetworkConfig.send_obj(self.sock, data)
            self.pushButtonJoin.setEnabled(True)
            self.lineEditName.setEnabled(False)
            self.pushButtonCreate.setText("取消游戏")
            self.is_create = True
        else:
            data = {
                "target": "server",
                "message": "quit"
            }
            NetworkConfig.send_obj(self.sock, data)
            self.pushButtonJoin.setEnabled(False)
            self.lineEditName.setEnabled(True)
            self.is_create = False
            self.pushButtonCreate.setText("创建游戏")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.is_connect:
            data = {
                "target": "server",
                "message": "quit"
            }
            self.keep_recv = False
            NetworkConfig.send_obj(self.sock, data)
        else:
            self.main_win.show()
        super().closeEvent(a0)


class NetworkPlayer(BaseWidget):
    """
    联机对战
    """
    dataSignal = pyqtSignal(dict, name='data')
    disconnectionSignal = pyqtSignal()

    def __init__(self, sock: socket.socket, name: str, parent=None):
        super().__init__(parent)
        self.name = name  # 对手昵称
        self.setupUi(self)
        self._chessboard = ChessBoard()
        self._is_finish = True
        self._color = 'w'
        self.is_my_turn = False
        self.keep_connection = True

        # 设置界面
        self.setupUi(self)
        self.setWindowTitle("对战中 对手: {}".format(self.name))
        self.labelStatus = QLabel("游戏状态：", self)
        self.labelStatus.resize(100, 20)
        self.labelStatusValue = QLabel("点击开始", self)
        self.labelStatusValue.resize(200, 20)
        self.labelStatusValue.setAlignment(Qt.AlignTop)
        self.labelStatus.move(630, 200)
        self.labelStatusValue.move(690, 204)

        self.buttonStart.clicked.connect(self.start)
        self.buttonGiveIn.clicked.connect(self.lose)
        self.win_label = QLabel(self)

        # 网络
        self.is_connected = True
        self.is_listening = True
        self.tcp_socket = sock
        self.labelStatusValue.setText("连接成功\n点击开始")
        Thread(target=self.recv_data, args=(self.tcp_socket, '')).start()

        self.dataSignal.connect(self.deal_data)
        self.disconnectionSignal.connect(self.disconnect_)

    def start(self):
        data = {
            "message": "action",
            "data": "restart",
            "target": "player"
        }
        NetworkConfig.send_obj(self.tcp_socket, data)
        self.labelStatusValue.setText("请求开始新游戏")
        self.is_my_turn = False

    def restart_func(self):
        self._chessboard = ChessBoard()
        if self._is_finish:
            if self.win_label is not None:
                self.win_label.close()
            self.win_label = None
            self._is_finish = False

    def lose(self):
        if self._is_finish:
            return
        if not self.is_connected:
            return
        else:
            data = {
                "message": "action",
                "data": "lose",
                "target": "player"
            }
            NetworkConfig.send_obj(self.tcp_socket, data)
            self.labelStatusValue.setText("对方胜利")
            if self.is_my_turn:
                self.change_color()
                self.win(color=self._color)
            else:
                self.win(color=self._color)

    def recv_data(self, sock: socket.socket):
        self.is_connected = True

        while self.keep_connection:
            try:
                recv = receive_sock(sock)
            except (ConnectionAbortedError, ConnectionResetError):
                if not self.keep_connection:
                    break
                self.is_connected = False
                self.disconnectionSignal.emit()
                break

            try:
                data = json.loads(recv)
                self.dataSignal.emit(data)
            except json.JSONDecodeError as e:
                logging.exception(str(e))
                logging.exception('error data: ' + recv)
                continue

        self.is_connected = False
        self.tcp_socket.close()

    def win(self, color):
        if color == 'b':
            win_pic = QPixmap("./sources/black_win.png")
            self.labelStatusValue.setText("黒棋胜利")
        else:
            win_pic = QPixmap("./sources/white_win.png")
            self.labelStatusValue.setText("白棋胜利")
        self.win_label = QLabel(parent=self)
        self.win_label.setPixmap(win_pic)
        self.win_label.resize(win_pic.size())
        self.win_label.move(50, 50)
        self.win_label.show()
        self._is_finish = True

    def deal_data(self, data: Dict[str, Any]):
        """
        处理接受的数据
        """
        print(data)
        if data['message'] == "action":
            if data["data"] == "restart":
                result = QMessageBox.information(self, "通知", "对方请求开始新游戏，是否同意？",
                                                 QMessageBox.Yes | QMessageBox.No)
                if result == QMessageBox.Yes:
                    data = {
                        "message": "reply",
                        "data": True,
                        "restart": "player"
                    }
                    NetworkConfig.send_obj(self.tcp_socket, data)
                    self.restart_func()
                    self._is_finish = False
                    self.is_my_turn = True
                    if self.is_my_turn:
                        self.labelStatusValue.setText("你的回合")
                    else:
                        self.labelStatusValue.setText("对手回合")
                else:
                    data = {
                        "message": "reply",
                        "data": False,
                        "restart": "player"
                    }
                    NetworkConfig.send_obj(self.tcp_socket, data)
                    self.labelStatusValue.setText("点击开始")

            if data["data"] == "lose":
                QMessageBox.information(self, "消息", "对方认输")
                if self.is_my_turn:
                    self.win(color=self._color)
                else:
                    self.change_color()
                    self.win(color=self._color)

            if data["data"] == "exit":
                self.keep_connection = False
                QMessageBox.information(self, "消息", "对方退出游戏，返回主菜单")
                self.back()

        elif data["message"] == "position":
            pos = data["data"]
            if self._chessboard.board[pos[1]][pos[0]] is not None:
                return
            legal_points = self._chessboard.legal_points(self._color)
            if len(legal_points) == 0:
                return
            self._chessboard.put_chessman(Chessman(self._color, self), pos)
            self.change_color()
            winner = self._chessboard.is_finish()
            if winner is not None:
                self.win(winner)
            self.is_my_turn = True
            self.labelStatusValue.setText("你的回合")

        elif data["message"] == "reply":
            if data["message"] == "restart":
                if data["data"]:
                    self.restart_func()
                else:
                    QMessageBox.information(self, "消息", "对方拒绝请求。")
                    self.labelStatusValue.setText("点击开始")
                    return
                if self.is_my_turn:
                    self.labelStatusValue.setText("你的回合")
                else:
                    self.labelStatusValue.setText("对方回合")

        elif data["message"] == "name":
            self.setWindowTitle("对战中 对手：{}".format(data["data"]))

    def change_color(self):
        if self._color == 'w':
            self._color = 'b'
        else:
            self._color = 'w'

    def disconnect_(self):
        QMessageBox.information(self, "消息", "连接断开，返回主界面")
        self.back()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.keep_connection = False
        if self.tcp_socket is not None and self.is_connected:
            logging.info("closeEvent called")
            data = {
                "message": "action",
                "data": "exit",
                "target": "player"
            }
            NetworkConfig.send_obj(self.tcp_socket, data)
            self.tcp_socket.close()
        return super().closeEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self._is_finish:
            return
        if not self.is_my_turn:
            return
        legal_points = self._chessboard.legal_points(self._color)
        if PIVOT[0] <= a0.x() <= PIVOT[0] + 8 * (GRID_SIZE + BORDER_SIZE) and \
                PIVOT[1] <= a0.y() <= PIVOT[1] + 8 * (GRID_SIZE + BORDER_SIZE):
            pos = trans_position(a0)
            if self._chessboard.board[pos[1]][pos[0]] is not None:
                return

            if pos in legal_points:
                self._chessboard.put_chessman(Chessman(self._color, self), pos)
                if self.tcp_socket is not None:
                    data = {
                        "message": "position",
                        "data": pos,
                        "target": "player"
                    }
                    NetworkConfig.send_obj(self.tcp_socket, data)

            winner = self._chessboard.is_finish()
            if winner is not None:
                self.win(winner)
                return
            self.is_my_turn = False
            self.labelStatusValue.setText("对方回合")
