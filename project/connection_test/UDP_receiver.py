import socket
import sys


if len(sys.argv) != 3:
    print("Usage: python script.py <ip_address> <port>")
    sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])

print("RECEIVER")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))
print("receiver started!")

while True:
    data, addr = sock.recvfrom(1024)        # buffer size is 1024 bytes
    print("received message:")
    print(data.decode("utf-8"))
    break
