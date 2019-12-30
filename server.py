import socket, json, logging
from threading import Thread
from typing import *

END_FLAG = 'END'
player_list = list()

def recv_sock(sock: socket.socket):
    """
    通过 socket 从网络接受数据
    """
    result = str()
    while True:
        data = sock.recv(1024).decode()
        if  END_FLAG in data:
            i = data.find('%s' % END_FLAG)
            if i != -1:
                result += data[:i]
                break
            else:
                raise ValueError()
        result += data
        if len(result) > 10240:
            result = str()
    return result

class Player(object):
    """
    玩家在服务器层面的抽象
    """
    def __init__(self, sock, name):
        self.sock = sock
        self.name = name
        self.target: Union[socket.socket, None] = None
        self.is_in_list = False
        Thread(target=self.receive_data).start()

    def deal_server_data(self, data: Dict[str, str]):
        if data['message'] == 'refresh':
            logging.info("Return the list of players.")


    def receive_data(self):
        while True:
            try:
                received_data = recv_sock(self.sock)
                json_data = json.loads(received_data)
                if json_data['target'] == 'player':
                    if self.target is not None:
                        str_data: str = json.dumps(json_data) + " " + END_FLAG
                        self.target.sendall(str_data.encode())
                elif json_data['target'] == 'server':
                    self.deal_server_data()
