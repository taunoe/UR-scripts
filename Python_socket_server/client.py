# Multithread Socket Server
# Client example
# 20.04.2023
# Tauno Erik

import socket
import signal
import sys

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 50001
ADDR = (SERVER_IP, SERVER_PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"Client connected to server at {SERVER_IP}:{SERVER_PORT}")

    connected = True
    while connected:
        msg = input("> ")

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")

interrupt_read, interrupt_write = socket.socketpair()

def handle_signal(signum, frame):
    print('Received signal: %s' % signum)
    print('Closing server socket...')
    interrupt_write.send(b'\0')
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    main()
