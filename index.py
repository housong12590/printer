import socket
import threading
import printer


def tcp_link(sock, addr):
    port = printer.open_port()
    while True:
        data = sock.recv(1024)
        if not data: break
        printer.send(port, data)
    printer.close(port)
    sock.close()
    print("接收数据完成")


def main():
    server = socket.socket()
    server.bind(('0.0.0.0', 9100))
    server.listen(5)
    print('服务启动完成,监听9100端口')
    while True:
        sock, addr = server.accept()
        print(addr)
        t = threading.Thread(target=tcp_link, args=(sock, addr))
        t.start()


if __name__ == '__main__':
    main()
