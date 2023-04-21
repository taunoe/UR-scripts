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

poses_index = 0
num_of_poses = 4
poses = [
    "(-0.05, -0.25, 0.15, -0.01, 3.11, 0.38)\n",
    "(0.05, -0.13, -0.15, 0.05, 3.10, 0.35)\n",
    "(0.15, -0.05, 0.08, 0.11, 2.90, 0.30)\n",
    "(-0.14, -0.20, -0.13, -0.18, 3.15, 0.20)\n"
]

def main():
    global x, y, z, rx, ry, rz
    global poses, poses_index

    for x in poses:
        print(x)

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

        connected = True
        pose = f"({x}, {y}, {z}, {rx},{ry},{rz})\n"

        server.send("Cognex".encode(FORMAT))

        while connected:
            msg_in = server.recv(SIZE).decode(FORMAT)

            if msg_in == "urready":
                if poses_index >= num_of_poses:
                    poses_index = 0
                print(f"Server saatis: {msg_in}")
                print(f"Index: {poses_index}")
                print(f"Saadan vastu: {poses[poses_index]}")
                server.send(poses[poses_index].encode(FORMAT))
                poses_index += 1
            else:
                print(f"Server saatis: {msg_in}")
    except:
        print("Ei saa serveriga ühendust")



interrupt_read, interrupt_write = socket.socketpair()

def handle_signal(signum, frame):
    print('Received signal: %s' % signum)
    print('Closing server socket...')
    interrupt_write.send(b'\0')
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

if __name__ == "__main__":
    main()
