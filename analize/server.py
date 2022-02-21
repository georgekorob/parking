import socket
from analize_func import AnalizeControl
from analize.settings import AN_IP, AN_PORT

analize_control = AnalizeControl()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((AN_IP, AN_PORT))
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
        analize_control.init(raw_data.split('\r\n')[8])
    elif command == 'calc':
        analize_control.calc(raw_data.split('\r\n')[8])
    elif command == 'destroy':
        analize_control.destroy()
        break
    if command in ['init', 'calc', 'destroy']:
        client_socket.send(set_headers())
    client_socket.close()

print('Shutdown!')
server.close()
