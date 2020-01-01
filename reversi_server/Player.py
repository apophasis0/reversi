import json
import logging
import socket
from threading import Thread
from typing import *

END_FLAG: str = 'END'
MAX_RECV_LEN: int = 10240


class Player(object):
    """
    玩家在服务器层面的抽象
    """

    def __init__(self, sock, name):
        self.sock: socket.socket = sock
        self.name = name
        self.target: Union[Player, None] = None
        self.is_in_queue = False
        self.player_list = PlayerList()
        Thread(target=self.receive_data).start()

    @staticmethod
    def send_obj(sock: socket.socket, data: Dict[str, Any]):
        str_data: str = json.dumps(data) + " " + END_FLAG
        sock.sendall(str_data.encode())

    @staticmethod
    def receive_sock(sock: socket.socket):
        """
        通过 socket 从网络接受数据
        """
        result = str()
        while True:
            data = sock.recv(1024).decode()
            if END_FLAG in data:
                i = data.find('%s' % END_FLAG)
                if i != -1:
                    result += data[:i]
                    break
                else:
                    raise ValueError()
            result += data
            if len(result) > MAX_RECV_LEN:
                result = str()
        return result

    def deal_server_data(self, json_data: Dict[str, Any]):
        if json_data['message'] == 'refresh':
            logging.info("返回玩家列表")
            data = {
                "message": "player_list",
                "data": [player.name for player in self.player_list.get_player_in_queue()]
            }
            Player.send_obj(self.sock, data)
            data = {
                "message": "get_name",
                "data": self.name
            }
            Player.send_obj(self.sock, data)

        elif json_data['message'] == 'battle':
            if json_data['data'] == self.name:
                logging.warning("尝试与自己进行游戏，发起人: %s" % self.name)
                data = {
                    "message": "response",
                    "type": "battle",
                    "data": False,
                    "info": "创建失败，不能与自己进行游戏"
                }
                Player.send_obj(self.sock, data)
                return
            self.target = self.player_list.get_player_by_name(json_data['data'])
            if self.target is not None:
                # 发给对手
                data = {
                    "message": "reply",
                    "type": "battle",
                    "data": True,
                    "name": self.name
                }
                Player.send_obj(self.target.sock, data)
                # 发给发起玩家
                data = {
                    "message": "reply",
                    "type": "battle",
                    "data": True,
                    "name": self.target.name
                }
                Player.send_obj(self.sock, data)
                logging.info("创建游戏，发起人: %s, 对手: %s" % (self.name, self.target.name))
            else:
                data = {
                    "message": "reply",
                    "type": "battle",
                    "data": True,
                    "info": "创建失败，找不到目标玩家"
                }
                Player.send_obj(self.sock, data)
                logging.warning("创建失败，找不到玩家 %s" % json_data['data'])

        elif json_data["message"] == "create":
            logging.info("玩家加入队列: %s" % json_data["data"])
            logging.info("当前玩家列表: %s" % str([p.name for p in self.player_list.get_player_in_queue()]))
            if json_data["data"] in [p.name for p in self.player_list.get_player_in_queue()]:
                data = {
                    "message": "reply",
                    "type": "create",
                    "data": "已经存在相同用户名的玩家，请重试"
                }
                Player.send_obj(self.sock, data)
                return
            self.name = json_data["data"]
            self.is_in_queue = True
            self.player_list.refresh()

        elif json_data["message"] == "quit":
            self.is_in_queue = False
            self.player_list.refresh()

        else:
            logging.error("无法处理的请求: %s" % json.dumps(json_data))

    def receive_data(self):
        while True:
            try:
                received_data = Player.receive_sock(self.sock)
                json_data = json.loads(received_data)
                if json_data['target'] == 'player':
                    if self.target is not None:
                        Player.send_obj(self.target.sock, json_data)
                elif json_data['target'] == 'server':
                    self.deal_server_data(json_data)

            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                logging.info("连接断开，玩家离开游戏")
                if self in self.player_list.get_players():
                    self.player_list.remove(self)
                    self.player_list.refresh()
                    logging.info("当前玩家列表: %s" % str([p.name for p in self.player_list.get_players()]))
                    logging.info("当前队列中玩家: %s" % str([p.name for p in self.player_list.get_player_in_queue()]))
            except json.JSONDecodeError:
                logging.exception("json 解析错误")


def singleton(cls):
    _instance = dict()

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner()


@singleton
class PlayerList(object):
    """
    玩家列表，使用单例模式实现
    """

    def __init__(self):
        self._players: Union[List[Player], None] = None

    def get_player_in_queue(self) -> List[Player]:
        res = list()
        for p in self._players:
            if p.is_in_queue:
                res.append(p)
        return res

    def get_player_by_name(self, name: str) -> Union[Player, None]:
        for p in self._players:
            if p.name == name:
                return p
        return None

    def get_players(self) -> List[Player]:
        return self._players

    def broadcast(self, data: Dict[str, Any]):
        """
        向所有玩家发送信息
        """
        for p in self._players:
            Player.send_obj(p.sock, data)

    def refresh(self):
        list_data = {
            "message": "player_list",
            "data": [p.name for p in self.get_player_in_queue()]
        }
        self.broadcast(list_data)

    def remove(self, player):
        self._players.remove(player)
