# 联机黑白棋

## 运行方法

本项目使用 PyQt5 开发，因此需先安装 PyQt5，运行时执行 main.py

```bash
$ pip install PyQt5     # 如果未安装PyQt5
$ python main.py
```

联机游戏使用的服务器程序位于 reviersi_server 包中，使用方法：

```bash
$ python server.py <server-port>    # server-port 是一个可选参数，默认为 12222 端口
```
