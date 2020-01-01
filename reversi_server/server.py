import logging
import socket
import sys
from threading import Thread

from reversi_server.Player import PlayerList, Player

player_list: PlayerList = PlayerList.__init__()


def start_listen(server_sock: socket.socket):
    global player_list
    logging.info("开始监听")
    while True:
        try:
            sock, addr = server_sock.accept()
            # 发送当前列表信息
            data = {
                "msg": "player_list",
                "data": [p.name for p in player_list.get_player_in_queue()]
            }
            Player.send_obj(sock, data)
            logging.info("当前玩家: %s" % str([p.name for p in player_list.get_players()]))
            logging.info("当前队列中玩家: %s" % str([p.name for p in player_list.get_player_in_queue()]))
            name = "玩家 {}".format(len(player_list.get_players()))
            player = Player(sock, name)
            player_list.get_players().append(player)
            data = {
                "message": "get_name",
                "data": name
            }
            Player.send_obj(sock, data)

        except OSError:
            logging.exception("监听失败, socket失效")
            break


if __name__ == '__main__':
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # port = int(sys.argv[0])
    port = 12332
    try:
        tcp_server.bind(("127.0.0.1", port))
        tcp_server.listen(32)
    except OSError as e:
        logging.exception("监听失败: " + str(e))
        logging.exception("{} 端口被占用".format(port))

    Thread(target=start_listen, args=(tcp_server,)).start()