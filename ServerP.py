import io
import json
import socket
from abc import ABC, abstractmethod
import cv2
import numpy as np
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
            try:
                if method == b'SOCKET':
                    data = ''
                    while raw_data:
                        raw_data = raw_data.split(b'<file>', 1)
                        data += raw_data[0].decode('utf-8')
                        if len(raw_data) > 1:
                            raw_data = raw_data[1]
                            break
                        else:
                            raw_data = client_socket.recv(1024)
                else:
                    data = raw_data.decode('utf-8').split('\r\n')[8]
                if command == 'init':
                    self.control = Control(data)
                elif command == 'action':
                    self.control.action(data, raw_data, client_socket)
                if command in ['init', 'action', 'destroy']:
                    client_socket.send(self.set_headers())
                if command == 'destroy':
                    self.control.destroy()
                    raise ConnectionError('Destroy!')
            except Exception as e:
                print(e)
            finally:
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
            # print(response.status_code, response.content)
        except Exception as e:
            print(errfstr.format(*args), end='')
            print(e)

    @staticmethod
    def request_get_from_base(url, errfstr='', *args):
        try:
            response = requests.get(url=url)
            # print(response.status_code, response.content)
            return response
        except Exception as e:
            print(errfstr.format(*args), end='')
            print(e)

    @staticmethod
    def get_file_client_socket(raw_data, client_socket, file_name):
        file = io.BytesIO()
        # file_for_save = open(f'{self.data["file_name"]}', 'wb')
        file.write(raw_data)
        while True:
            line = client_socket.recv(1024)  # получаем байтовые строки
            file.write(line)  # пишем байтовые строки в файл на сервере
            if not line:
                break
        file.name = file_name
        file.seek(0)
        return file

    @staticmethod
    def buffer_file_from_frame(frame_to_buf, filename):
        io_buf_bytes = io.BytesIO(cv2.imencode('.jpg', frame_to_buf)[1].tobytes())
        io_buf_bytes.name = filename
        return io.BufferedReader(io_buf_bytes)

    @staticmethod
    def frame_from_buffer_file(bytesio):
        file_bytes = np.asarray(bytearray(bytesio.read()), dtype=np.uint8)
        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
