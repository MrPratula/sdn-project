
import socket
import sys


if len(sys.argv) != 3:
    print("Usage: python script.py <ip_address> <port>")
    sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])

print("SENDER")

message = b"mi piace la pizza UDP"

print("sender started!")
print("Sending message to {}:{}...".format(ip, port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (ip, port))

print("message sent!")
