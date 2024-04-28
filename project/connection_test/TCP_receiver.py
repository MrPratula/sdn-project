
import socket
import sys


if len(sys.argv) != 3:
    print("Usage: python3 TCP_receiver.py <ip_address> <port>")
    sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])

print("TCP RECEIVER")
print("receiver started!")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the server address and port
    server_socket.bind((ip, port))

    # Listen for incoming connections
    server_socket.listen()

    print("Server is listening for incoming connections...")

    while True:
        # Accept a new connection
        connection, client_address = server_socket.accept()
        print("Connection from:", client_address)

        # Receive the message
        message = connection.recv(1024).decode()
        if message:
            print("Received message:")
            print(message)

        # Close the connection
        connection.close()

        break
