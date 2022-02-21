import json
import pickle
import socket
from abc import ABC, abstractmethod
import requests


class ServerIPCam:
    control = []

    def __init__(self, Control, IP, PORT):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen(2)
        print("Working...")
        while True:
            # начинаем принимать соединения
            client_socket, address = server.accept()
            print('Connected:', address)
            # получаем команду
            raw_data = client_socket.recv(1024)
            method, command, raw_data = raw_data.split(b' ', 2)
            command = command.decode('utf-8').strip('/')
            print(command)
            if method == b'SOCKET':
                raw_data = raw_data.split(b'<file>', 1)
                data = raw_data[0].decode('utf-8')
                raw_data = raw_data[1] if len(raw_data) > 1 else b''
            else:
                data = raw_data.decode('utf-8').split('\r\n')[8]
            if command == 'init':
                self.control = Control(data)
            elif command == 'action':
                self.control.action(data, raw_data, client_socket)
            elif command == 'destroy':
                self.control.destroy()
                break
            if command in ['init', 'action', 'destroy']:
                client_socket.send(self.set_headers())
            client_socket.close()
        print('Shutdown!')
        server.close()

    @staticmethod
    def set_headers(content=''):
        HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        content = content.encode('utf-8')
        return HDRS.encode('utf-8') + content


class ControlClass(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def action(self, *args, **kwargs):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @staticmethod
    def request_to_srv(ip, port, cmd, data, file=None):
        sock = socket.socket()
        sock.connect((ip, int(port)))
        sock.send((f'SOCKET {cmd} ' + json.dumps(data)).encode('utf-8'))
        if file:
            sock.send('<file>'.encode('utf-8'))
            line = file.read(1024)
            while (line):
                sock.send(line)
                line = file.read(1024)
        sock.close()

    @staticmethod
    def request_to_base(url, data, files=None, errfstr='', *args):
        try:
            response = requests.patch(url=url, files=files, data=data)
            print(response.status_code, response.content)
        except Exception as e:
            print(errfstr.format(*args), end='')
            print(e)
