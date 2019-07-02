from configparser import ConfigParser
import serial

cp = ConfigParser()
cp.read('printer.cfg')

mode = cp.get('printer', 'mode')

if mode == 'serial':
    portName = cp.get('serial', 'portName')
    baudRate = cp.get('serial', 'baudRate')
else:
    portName = cp.get('parallel', 'portName')


def open_port():
    if mode == 'serial':
        port = serial.Serial(portName, baudRate)
    else:
        port = open(portName, 'wb')
    print('打开端口[%s]' % portName)
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
    print('关闭端口[%s]' % portName)
