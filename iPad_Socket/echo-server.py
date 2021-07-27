#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# HOST = '192.168.0.8'  # iPad Address
# HOST = '127.0.1.1'  # Raspberry Pi address
# HOST = ''  # iPad Address
PORT = 65432       # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # print(s)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(repr(data))
            conn.sendall(b'message_received from PC ')
            if not data:
                break
            conn.sendall(data)
