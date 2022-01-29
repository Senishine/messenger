import time
from socket import socket, AF_INET, SOCK_STREAM
from utils import send_message


def send_message_to_users(account_name, room_name, message):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(('localhost', 7777))
        message_dict = {
            "action": "msg",
            "time": time.time(),
            "to": room_name,
            "from": account_name,
            "message": message
        }
        send_message(message_dict, s)


if __name__ == '__main__':
    while True:
        send_message_to_users(account_name='guest', room_name='chat', message=input('Input message: '))
