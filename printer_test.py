from socket import socket
import os
import sys
from time import sleep

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    test_file = os.path.join(dir_path, 'print_test.temp')
    with open(test_file, 'rb') as f:
        sock = socket()
        sock.connect(('localhost', 9100))
        sock.send(f.read())
        sleep(1)
        sock.close()
