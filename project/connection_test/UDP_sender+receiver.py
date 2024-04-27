
import socket
import multiprocessing
import time

ip = "127.0.0.1"
port = 12345


def main():
    print("SENDER\t\t\t\t\t\t\t\t\t\t\tRECEIVER")

    sender = multiprocessing.Process(name="sender", target=start_UDP_sender)
    receiver = multiprocessing.Process(name="receiver", target=start_UDP_receiver)

    receiver.start()
    time.sleep(1)
    sender.start()


def start_UDP_sender():

    message = b"mi piace la pizza UDP"

    print("sender started!")
    print("Sending message to {}:{}...".format(ip, port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (ip, port))

    print("message sent!")


def start_UDP_receiver():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print("\t\t\t\t\t\t\t\t\t\t\t\treceiver started!")

    while True:
        data, addr = sock.recvfrom(1024)        # buffer size is 1024 bytes
        print("\t\t\t\t\t\t\t\t\t\t\t\treceived message:")
        print("\t\t\t\t\t\t\t\t\t\t\t\t{}".format(data.decode("utf-8")))
        break


if __name__ == "__main__":
    main()
