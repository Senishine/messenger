import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from messages import MessageType, ServerResponseFieldName, ResponseCode, ClientRequestFieldName
from utils import send_message, get_data


def create_presence_msg(account_name, status=''):
    return {
        'action': MessageType.PRESENCE.value,
        'time': time.time(),
        'type': 'status',
        'user': {
            'account_name': account_name,
            'status': status
        }
    }


def create_client_socket(address, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((address, port))
    return s


def create_message(account_name, recipient_name, message):
    message_dict = {
        "action": "msg",
        "time": time.time(),
        "to": recipient_name,
        "from": account_name,
        "message": message
    }
    return message_dict


class ReceiverThread(Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket
        self.__stopped = False

    def stop(self):
        self.__stopped = True

    @property
    def stopped(self):
        return self.__stopped

    def run(self):
        while not self.__stopped:
            data = get_data(self.socket)

            response_code = data.get(ServerResponseFieldName.RESPONSE.value)
            if response_code == ResponseCode.OK:
                return
            elif response_code is not None:
                print(f"Exit due to error code from server code={response_code},"
                      f" msg={data.get(ServerResponseFieldName.ERROR.value)}")
                self.stop()
                return

            action = data.get(ClientRequestFieldName.ACTION.value)
            if action != MessageType.MESSAGE.value:
                print(f"Received unknown message from server msg={data}")
                self.stop()
                return

            try:
                print(f'{data["from"]}: {data["message"]}')
            except ValueError:
                print(f"Invalid msg format, msg={data}")
                self.stop()


def main():
    cl_soc = create_client_socket(address='localhost', port=7777)
    client_name = input('Input your name: ')
    send_message(create_presence_msg(client_name), cl_soc)
    receiver = ReceiverThread(cl_soc)
    receiver.start()
    while not receiver.stopped:
        friend = input('Input friend\'s name: ')
        if friend == ':quit':
            break
        while True:
            mes = input('Input your message: ')
            if mes == ':quit':
                break
            send_message(create_message(client_name, friend, mes), cl_soc)
    receiver.stop()
    receiver.join(5)
    cl_soc.close()


if __name__ == '__main__':
    main()
