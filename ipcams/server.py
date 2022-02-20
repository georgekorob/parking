import json
import socket
from ip_cam_func import CameraControl

camera_control = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8001))
server.listen(2)
print("Working...")


def set_headers(content=''):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    content = content.encode('utf-8')
    return HDRS.encode('utf-8') + content


while True:
    # начинаем принимать соединения
    client_socket, address = server.accept()
    print('Connected:', address)

    # получаем команду
    raw_data = client_socket.recv(1024).decode('utf-8')
    command = raw_data.split('\r\n')[0].split()[1][1:-1]
    print(command)
    if command == 'init':
        cameras = json.loads(raw_data.split('\r\n')[8])
        print(cameras)
        camera_control = CameraControl(cameras)
    elif command == 'shoot':
        id_cameras = json.loads(raw_data.split('\r\n')[8])
        print(id_cameras)
        camera_control.shoot(id_cameras)
    elif command == 'destroy':
        camera_control.destroy()
        break
    if command in ['init', 'shoot', 'destroy']:
        client_socket.send(set_headers())
    client_socket.close()

print('Shutdown!')
server.close()
