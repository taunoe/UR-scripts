# Multithread Socket Server
# Stared: 20.04.2023
# Edited: 21.04.2023
# Tauno Erik

# Two clients:
#   1. Universal Robot
#   2. Cognex Designer

import socket
import threading
import signal
import sys



# If runs in Cognex Designer PC:
#SERVER_IP = '192.168.0.101'
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 50000

SIZE = 1024
FORMAT = "ASCII" #"utf-8"

MSG_DISCONNECT = "!DISCONNECT"
MSG_NEWPOSE    = "newpose"
MSG_UR_READY   = "urready"


# UR pose
x  = -0.05
y  = -0.25
z  = 0.15
rx = -0.01
ry = 3.11
rz = 0.38
#pose = f"({x}, {y}, {z}, {rx},{ry},{rz})\n"


def list_to_dict(l):
  assert type(l) is list
  return {'x' : l[0], 'y' : l[1], 'z' : l[2], 'rx' : l[3], 'ry' : l[4], 'rz' : l[5]}

def dict_to_list(p):
  assert type(p) is dict
  return [p['x'], p['y'], p['z'], p['rx'], p['ry'], p['rz']]

clients = []
ur_id = 0
cognex_id = 0

def handle_client(client, addr):
    global x, ur_id, cognex_id

    clients.append(client)

    print("Client " + addr[0] + ":" + str(addr[1]) + " connected.")

    connected = True

    while connected:
        msg_in = client.recv(SIZE).decode(FORMAT)

        if msg_in != "":
            if msg_in == "ur_id":
                # Registreerime roboti klient ID
                print(f"UR index {clients.index(client)}")
                ur_id = clients.index(client)
                if ur_id == 0:
                    cognex_id = 1
                else:
                    cognex_id = 0
            elif msg_in == MSG_DISCONNECT:
                # Ühendame kliendi lahti
                print(f"Klient {addr} saatis: {msg_in}")
                connected = False
            elif msg_in == MSG_NEWPOSE:
                # Saadame robotile uue pose
                print(f"UR {addr} küsis: {msg_in}")
                x = x + 0.01
                pose = f"({x}, {y}, {z}, {rx},{ry},{rz})\n"
                send_msg = pose
                print(f"Server saadab: {pose}")
                clients[ur_id].send(send_msg.encode(FORMAT))
                #client.send(send_msg.encode(FORMAT))
            elif msg_in == "urready":
                # UR on valmis, Cognex tee pilti
                print("UR on valmis")
                send_msg = "urready"
                clients[cognex_id].send(send_msg.encode(FORMAT))
            elif msg_in == "Cognex":
                print(f"Cognex ühendatud")
            else:
                print(f"Klient saatis {msg_in}")

    client.close()
    print("Close connection")


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

    


### CTRL+c

interrupt_read, interrupt_write = socket.socketpair()

def handle_signal(signum, frame):
    print('Received signal: %s' % signum)
    print('Closing server socket...')
    interrupt_write.send(b'\0')
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)



if __name__ == "__main__":
    main()
    
    
