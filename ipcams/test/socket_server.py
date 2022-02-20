import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8001))
server.listen(2)
print("Working...")

while True:
    # начинаем принимать соединения
    client_socket, address = server.accept()

    # выводим информацию о подключении
    print('Connected:', address)

    # получаем название файла
    namefile = client_socket.recv(1024).decode('utf-8')

    # открываем файл в режиме байтовой записи
    file_for_save = open(namefile, 'wb')

    while True:

        # получаем байтовые строки
        line = client_socket.recv(1024)

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
