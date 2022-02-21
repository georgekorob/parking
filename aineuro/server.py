import socket
from ai_neuro_func import AINeuroControl
from aineuro.settings import AI_IP, AI_PORT

neuro_control = AINeuroControl()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((AI_IP, AI_PORT))
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
    raw_data = raw_data.split('\r\n')
    command = raw_data[0].split()[1].strip('/')
    print(command)
    if command == 'init':
        neuro_control.init(raw_data[8])
    elif command == 'calc':
        neuro_control.calc(client_socket, raw_data)
    elif command == 'destroy':
        neuro_control.destroy()
        break
    if command in ['init', 'calc', 'destroy']:
        client_socket.send(set_headers())
    client_socket.close()

print('Shutdown!')
server.close()
