import socket
from ip_cam_func import IPCameraControl
from ipcams.settings import IPCAM_IP, IPCAM_PORT

camera_control = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IPCAM_IP, IPCAM_PORT))
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
    command = raw_data.split('\r\n')[0].split()[1].strip('/')
    print(command)
    if command == 'init':
        camera_control = IPCameraControl(raw_data.split('\r\n')[8])
    elif command == 'shoot':
        camera_control.shoot(raw_data.split('\r\n')[8])
    elif command == 'destroy':
        camera_control.destroy()
        break
    if command in ['init', 'shoot', 'destroy']:
        client_socket.send(set_headers())
    client_socket.close()

print('Shutdown!')
server.close()
