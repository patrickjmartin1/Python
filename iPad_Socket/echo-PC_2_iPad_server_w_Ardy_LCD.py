#!/usr/bin/env python3
import serial # Serial imported for Serial communication
import time  # Required to use delay functions
import socket

ard_ser = serial.Serial('COM3', 9600, timeout=2)  # Create Serial port object called ard_ser for arduino_serial
time.sleep(1) #give the connection a second to settle

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
HOST = '192.168.0.8'  # IP Address of this laptop
# HOST = '127.0.1.1'  # Raspberry Pi address
# HOST = ''  # iPad Address
PORT = 65432       # Port to listen on (non-privileged ports are > 1023)

pc_confirmation_msg = 'message_received from PC '

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # print(s)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data_from_ipad = conn.recv(1024)
            print(data_from_ipad.decode())
            conn.sendall(pc_confirmation_msg.encode())
            ard_ser.write(data_from_ipad)
            time.sleep(1)
            data_from_ardy = ard_ser.readline()  # the last bit gets rid of the new-line chars
            if data_from_ardy:
                try:
                    print(data_from_ardy.decode().rstrip('\n'))
                except:
                    print(data_from_ardy.decode())
            conn.sendall(data_from_ardy)
