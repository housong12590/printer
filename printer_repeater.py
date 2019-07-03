from configparser import ConfigParser
from serial import Serial
from socket import socket
import logging
import os
import sys

cp = ConfigParser()

dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))

cp.read(os.path.join(dir_path, 'printer_repeater.cfg'))

log_file = open(os.path.join(dir_path, 'app.log'), encoding="utf-8", mode="a")

logging.basicConfig(stream=log_file,
                    format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%M-%d %H:%M:%S",
                    level=logging.DEBUG)

logging.debug('加载配置文件')

mode = cp.get('printer', 'mode')

if mode == 'serial':
    portName = cp.get('serial', 'portName')
    baudRate = cp.get('serial', 'baudRate')
    logging.debug('初始化端口信息: %s %s' % (portName, baudRate))
else:
    portName = cp.get('parallel', 'portName')
    logging.debug('初始化端口信息: %s' % (portName))


def open_port():
    if mode == 'serial':
        port = Serial(portName, baudRate)
    else:
        port = open(portName, 'wb')
    logging.debug('打开端口[%s]' % portName)
    return port


def send(port, data):
    try:
        if mode == 'serial':  # 串口
            port.write(data)
            port.flushOutput()
        else:  # 并口
            port.write(data)
            port.flush()
    except Exception as e:
        logging.error('写入数据失败 ' + str(e))


def close(port):
    port.close()
    logging.debug('关闭端口[%s]' % portName)


def tcp_link(sock, addr):
    try:
        port = open_port()
        while True:
            data = sock.recv(1024)
            if not data: break
            send(port, data)
        close(port)
        sock.close()
        logging.debug("接收数据完成")
    except Exception as e:
        logging.error('接收数据失败 ' + str(e))


def main():
    server = socket()
    server.bind(('0.0.0.0', 9100))
    server.listen(5)
    logging.debug('服务启动完成, 监听9100端口, 等待接收数据...')
    while True:
        sock, addr = server.accept()
        logging.debug('%s:%s 已连接' % (addr[0], addr[1]))
        tcp_link(sock, addr)


if __name__ == '__main__':
    main()
