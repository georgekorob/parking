import socket
from pathlib import Path
import sys
import requests

shotspath = Path(__file__).resolve().parent.parent / 'camerashots'
namefile = shotspath / '001' / 'frame.jpg'
file = open(namefile, 'rb')

ip = "127.0.0.1"
port = 8001

# создаём сокет для подключения
sock = socket.socket()
sock.connect((ip, port))

# имя файла отправляем серверу
sock.send('start'.encode('utf-8'))
sock.send(namefile.name.encode('utf-8'))

# открываем файл в режиме байтового чтения
file_to_send = open(namefile, "rb")

# читаем строку
line = file_to_send.read(1024)

while (line):
    # отправляем строку на сервер
    sock.send(line)
    line = file_to_send.read(1024)

file_to_send.close()
sock.close()
