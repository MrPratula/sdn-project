
import socket
import sys


if len(sys.argv) != 3:
    print("Usage: python script.py <ip_address> <port>")
    sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])

print("TCP SENDER")
print("sender started!")

message = "mi piace la pizza pepperoni TCP"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the server
    client_socket.connect((ip, port))

    # Send the message
    print("sending message to {}:{}...".format(ip, port))
    client_socket.sendall(message.encode())
    print("message sent")
