import socket, json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8002))
server.listen(2)
print("Working...")

while True:
    # начинаем принимать соединения
    client_socket, address = server.accept()

    # выводим информацию о подключении
    print('Connected:', address)

    line = client_socket.recv(1024)
    method, command, line = line.split(b' ', 2)
    data, line = line.split(b'<file>', 1)
    data = json.loads(data)
    file_name = data['file_name']
    camera_id = data['camera_id']
    # открываем файл в режиме байтовой записи
    file_for_save = open(f'{file_name}.jpg', 'wb')
    file_for_save.write(line)
    iter = 0

    while True:

        # получаем байтовые строки
        line = client_socket.recv(1024)
        if iter < 50:
            print(line)
        iter += 1
        # пишем байтовые строки в файл на сервере
        file_for_save.write(line)

        if not line:
            break

    # HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    # content = 'Well done, buddy!'.encode('utf-8')
    # client_socket.send(HDRS.encode('utf-8') + content)
    file_for_save.close()
    client_socket.close()

    print('File received')

print('Shutdown!')
server.close()
