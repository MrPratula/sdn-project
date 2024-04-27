
import multiprocessing
import socket
import time


ip = "127.0.0.1"
port = 1234
space = "\t\t\t\t\t\t\t\t\t\t\t\t"


def main():

    print("SENDER\t\t\t\t\t\t\t\t\t\t\tRECEIVER")

    sender = multiprocessing.Process(name="sender", target=start_TCP_sender)
    receiver = multiprocessing.Process(name="receiver", target=start_TCP_receiver)

    receiver.start()
    time.sleep(1)
    sender.start()


def start_TCP_sender():

    print("sender started!")

    message = "mi piace la pizza pepperoni TCP"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((ip, port))

        # Send the message
        print("sending message to {}:{}...".format(ip, port))
        client_socket.sendall(message.encode())
        print("message sent")


def start_TCP_receiver():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the server address and port
        server_socket.bind((ip, port))

        # Listen for incoming connections
        server_socket.listen()

        print(space, "Server is listening for incoming connections...")

        while True:
            # Accept a new connection
            connection, client_address = server_socket.accept()
            print(space, "Connection from:", client_address)

            # Receive the message
            message = connection.recv(1024).decode()
            if message:
                print(space, "Received message:")
                print(space, message)

            # Close the connection
            connection.close()

            break


if __name__ == "__main__":
    main()
