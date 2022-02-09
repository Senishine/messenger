from socket import socket, AF_INET, SOCK_STREAM


def receive_messages(host='localhost', port=7777):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            data = sock.recv(1024)
            print(f'Received message {data.decode("utf-8")}')


if __name__ == '__main__':
    receive_messages()
