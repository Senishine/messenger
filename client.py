# *В следующем уроке мы будем изучать дескрипторы и метаклассы.
# Но вы уже сейчас можете перевести часть кода из функционального стиля в объектно-ориентированный.
# Создайте классы «Клиент» и «Сервер», а используемые функции превратите в методы классов.
import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from messages import MessageType, ServerResponseFieldName, ResponseCode, ClientRequestFieldName
from utils import send_message, get_data


class ReceiverThread(Thread):
    def __init__(self, sock):
        super().__init__()
        self.__socket = sock
        self.__stopped = False

    def stop(self):
        self.__stopped = True

    @property
    def stopped(self):
        return self.__stopped

    def run(self):
        while not self.__stopped:
            data = get_data(self.__socket)

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


class Client:
    def __init__(self, account_name, address='localhost', port=7777):
        self.__account = account_name
        self.__address = address
        self.__port = port
        self.__connected = False
        self.__sock = None
        self.__stopped = False
        self.__receiver = None

    @staticmethod
    def __create_message(account_name, recipient_name, message):
        message_dict = {
            "action": "msg",
            "time": time.time(),
            "to": recipient_name,
            "from": account_name,
            "message": message
        }
        return message_dict

    @staticmethod
    def __create_presence_msg(account_name, status=''):
        return {
            'action': MessageType.PRESENCE.value,
            'time': time.time(),
            'type': 'status',
            'user': {
                'account_name': account_name,
                'status': status
            }
        }

    def connect(self):
        if self.__connected:
            raise ValueError('Client already connected')
        self.__connected = True
        self.__sock = socket(AF_INET, SOCK_STREAM)
        self.__sock.connect((self.__address, self.__port))
        send_message(self.__create_presence_msg(self.__account), self.__sock)
        self.__receiver = ReceiverThread(self.__sock)
        self.__receiver.start()

    def disconnect(self):
        self.__stopped = True
        if self.__receiver:
            self.__receiver.stop()

    def disconnected(self) -> bool:
        return self.__stopped

    def await_termination(self, timeout=5):
        if not self.__receiver:
            return
        self.__receiver.join(timeout)
        self.__sock.close()

    def send(self, recipient_name, message):
        if self.__sock is None:
            raise ValueError('Client is not initialised')
        send_message(self.__create_message(self.__account, recipient_name, message), self.__sock)


def main():
    client_name = input('Input your name: ')
    client = Client(client_name, address='localhost', port=7777)
    client.connect()

    while not client.disconnected():
        friend = input('Input friend\'s name: ')
        if friend == ':quit':
            break
        while True:
            mes = input('Input your message: ')
            if mes == ':quit':
                break
            client.send(friend, mes)

    client.await_termination()


if __name__ == '__main__':
    main()
