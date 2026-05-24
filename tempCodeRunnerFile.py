import socket
import threading
from encryption import encrypt, decrypt
from datetime import datetime

server = socket.socket()
server.bind(("localhost", 12345))
server.listen(5)

print("Server Started ✅")

clients = {}
          
def broadcast(msg, exclude=None):
    for c in clients:
        if c != exclude:
            try:
                c.send(encrypt(msg))
            except:
                pass

def handle(client):
    username = clients[client]
    broadcast(f"ONLINE:{username}", client)

    while True:
        try:
            msg = decrypt(client.recv(1024))

            if msg == "__typing__":
                broadcast(f"TYPING:{username}", client)
                continue

            time = datetime.now().strftime("%H:%M")

            # ---------------- OLD FORMAT (KEEP) ----------------
            old_msg = f"{username} [{time}]: {msg}"

            # ---------------- NEW FORMAT (ADD) ----------------
            # new_msg = f"{username}|{time}|{msg}"

            print(old_msg)

            broadcast(old_msg, client)
            

        except:
            del clients[client]
            broadcast(f"OFFLINE:{username}", client)
            client.close()
            break

while True:
    client, addr = server.accept()
    print("Connected:", addr)

    username = decrypt(client.recv(1024))
    clients[client] = username

    for c in clients:
        if c != client:
            client.send(encrypt(f"ONLINE:{clients[c]}"))

    threading.Thread(target=handle, args=(client,), daemon=True).start()