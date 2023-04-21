# Multithread Socket Server
# Client example: Cognex simulator
# Started 20.04.2023
# Edited  21.04.2023
# Tauno Erik

import socket
import signal
import sys

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 50000

SIZE = 1024
FORMAT = "ASCII" #"utf-8"
DISCONNECT_MSG = "!DISCONNECT"

# UR pose
x  = -0.05
y  = -0.25
z  = 0.15
rx = -0.01
ry = 3.11
rz = 0.38
#pose = f"({x}, {y}, {z}, {rx},{ry},{rz})\n"

def main():
    global x, y, z, rx, ry, rz

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

    connected = True
    pose = f"({x}, {y}, {z}, {rx},{ry},{rz})\n"

    server.send("Cognex".encode(FORMAT))
    print("Saadan")

    while connected:
        msg_in = server.recv(SIZE).decode(FORMAT)

        if msg_in == "urready":
            print(f"Server saatis: {msg_in}")
            print(f"Saadan vastu: {pose}")
            server.send(pose.encode(FORMAT))
        else:
            print(f"Server saatis: {msg_in}")


        #if msg == DISCONNECT_MSG:
        #    connected = False
        #else:
        #    msg = client.recv(SIZE).decode(FORMAT)
        #    print(f"[SERVER] {msg}")



interrupt_read, interrupt_write = socket.socketpair()

def handle_signal(signum, frame):
    print('Received signal: %s' % signum)
    print('Closing server socket...')
    interrupt_write.send(b'\0')
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    main()
