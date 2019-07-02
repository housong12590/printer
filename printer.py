from configparser import ConfigParser
import serial
import socket
import threading
import logging
import os
import sys

cp = ConfigParser()

dirpath = os.path.dirname(os.path.realpath(sys.argv[0]))

cp.read(os.path.join(dirpath, 'printer.cfg'))

logging.basicConfig(filename=os.path.join(dirpath, 'app.log'), filemode="w",
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
        port = serial.Serial(portName, baudRate)
    else:
        port = open(portName, 'wb')
    logging.debug('打开端口[%s]' % portName)
    return port


def send(port, data):
    if mode == 'serial':  # 串口
        port.write(data)
        port.flushOutput()
    else:  # 并口
        port.write(data)
        port.flush()


def close(port):
    port.close()
    logging.debug('关闭端口[%s]' % portName)


def tcp_link(sock, addr):
    port = open_port()
    while True:
        data = sock.recv(1024)
        if not data: break
        send(port, data)
    close(port)
    sock.close()
    logging.debug("接收数据完成")


def main():
    server = socket.socket()
    server.bind(('0.0.0.0', 9100))
    server.listen(5)
    logging.debug('服务启动完成, 监听9100端口, 等待接收数据...')
    while True:
        sock, addr = server.accept()
        logging.debug('%s:%s 已连接' % (addr[0], addr[1]))
        t = threading.Thread(target=tcp_link, args=(sock, addr))
        t.start()


if __name__ == '__main__':
    main()
