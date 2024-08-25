# Server Program to handle Several Clients to communicate each other using Threads

import socket
import threading

HOST = "127.0.0.1"
PORT = 5454
FORMAT = 'UTF-8'
HEADER = 64
DISCONNECT_MESSAGE = "bye"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    connected = True
    while connected:
        msg_length = client_socket.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            message = client_socket.recv(msg_length).decode(FORMAT)
            if message.split(":")[1].strip() == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{address}] {message}")
            broadcast(message, client_socket)

    client_socket.close()
    print(f"[DISCONNECT] {address} disconnected.")

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode(FORMAT))

def start_server():
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
