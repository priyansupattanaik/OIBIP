import socket
import threading

def handle_client(client_socket, clients, usernames, chatrooms):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        client_socket.send("ACK".encode('utf-8'))
        chatroom = client_socket.recv(1024).decode('utf-8')
        client_socket.send("ACK".encode('utf-8'))

        clients[client_socket] = chatroom
        usernames[client_socket] = username

        print(f"{client_socket.getpeername()} logged in as {username}")

        broadcast_message(f"{username} has joined the chat", client_socket, clients, chatroom)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{username}: {message}")
                broadcast_message(f"{username}: {message}", client_socket, clients, chatroom)
            else:
                break
    except ConnectionResetError:
        print(f"{username} has disconnected")
    finally:
        client_socket.close()
        del clients[client_socket]
        del usernames[client_socket]
        broadcast_message(f"{username} has left the chat", client_socket, clients, chatroom)

def broadcast_message(message, client_socket, clients, chatroom):
    for client, room in clients.items():
        if client != client_socket and room == chatroom:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to {client.getpeername()}: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen()

    clients = {}
    usernames = {}
    chatrooms = {}

    print("Server started...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")
        threading.Thread(target=handle_client, args=(client_socket, clients, usernames, chatrooms)).start()

if __name__ == "__main__":
    main()
