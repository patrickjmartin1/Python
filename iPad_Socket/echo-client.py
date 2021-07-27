#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        s.connect((HOST, PORT))
        s.sendall(b'Hello from my PC')
        data = s.recv(1024)
        if not data:
            raise Exception("Data not received by Client")
            break

print('Received', repr(data))