# Multithread Socket Server
# 20.04.2023
# Tauno Erik

import socket
import threading
import signal
import sys


#SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_IP = '127.0.1.1'
SERVER_PORT = 50001

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def handle_client(client_socket, addr):
    print("Client" + addr[0] + ":" + addr[1] + "connected.")

    connected = True

    while connected:
        msg = client_socket.recv(SIZE).decode(FORMAT)

        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"

        send_msg = "(0.0, 0.1, 0.2, 0.3, 0.4, 0.5)"
        client_socket.send(send_msg.encode(FORMAT))

    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()

    print(f"Server {SERVER_IP}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



interrupt_read, interrupt_write = socket.socketpair()

def handle_signal(signum, frame):
    print('Received signal: %s' % signum)
    print('Closing server socket...')
    interrupt_write.send(b'\0')
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)


if __name__ == "__main__":
    main()
