#!/usr/bin/env python3

#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


message_from_client = b'Hello, from the client!'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(message_from_client)
    data = s.recv(1024)

print('Received', repr(data))