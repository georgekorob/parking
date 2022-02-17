import socket
from settings import BASE_IP, BASE_PORT, AI_IP, AI_PORT, AN_IP, AN_PORT



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((AI_IP, AI_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
