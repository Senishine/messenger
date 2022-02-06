# *В следующем уроке мы будем изучать дескрипторы и метаклассы.
# Но вы уже сейчас можете перевести часть кода из функционального стиля в объектно-ориентированный.
# Создайте классы «Клиент» и «Сервер», а используемые функции превратите в методы классов.
from log.client_log_config import logging
import time
from queue import Queue, Empty
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from messages import MessageType, ServerResponseFieldName, ClientRequestFieldName
from utils import send_message, get_data

logger = logging.getLogger('gb.client')


class ReceiverThread(Thread):
    def __init__(self, sock: socket, responses_queue: Queue, message_listener):
        super().__init__()
        self.__socket = sock
        self.__responses_queue = responses_queue
        self.__message_listener = message_listener
        self.__stopped = False

    def stop(self):
        self.__stopped = True

    @property
    def stopped(self):
        return self.__stopped

    def run(self):
        while not self.__stopped:
            data = get_data(self.__socket)
            logger.debug("Received message from server [msg=%s]", data)
            response_code = data.get(ServerResponseFieldName.RESPONSE.value)
            if isinstance(response_code, int):
                self.__responses_queue.put(data)
                continue

            action = data.get(ClientRequestFieldName.ACTION.value)
            if action != MessageType.MESSAGE.value:
                print(f"Received unknown message from server msg={data}")
                self.stop()
                return
            self.__message_listener(data)


class SendTask:
    def __init__(self, msg: dict, result_callback):
        self.msg = msg
        self.result_callback = result_callback


class SenderThread(Thread):

    def __init__(self, sock: socket, responses_queue: Queue):
        super().__init__()
        self.__socket = sock
        self.__task_queue = Queue()
        self.__responses_queue = responses_queue
        self.__stopped = False

    def submit_task(self, msg: dict, callback):
        self.__task_queue.put(SendTask(msg, callback))

    def run(self):
        while not self.__stopped:
            try:
                to_send: SendTask = self.__task_queue.get(timeout=1)
                logger.debug("Sending message to server [msg=%s]", to_send.msg)
                send_message(to_send.msg, self.__socket)
                response_from_server = self.__responses_queue.get()
                logger.debug("Received response from server [msg=%s]", response_from_server)
                to_send.result_callback(response_from_server)
            except Empty:
                pass


def create_socket() -> socket:
    return socket(AF_INET, SOCK_STREAM)


class Client():

    def __init__(self, message_listener, address='localhost', port=7777):
        self.__message_listener = message_listener
        self.__address = address
        self.__port = port
        self.__account = None
        self.__connected = False
        self.__sock = None
        self.__stopped = False
        self.__receiver = None
        self.__task_sender = None

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

    @staticmethod
    def __create_get_contacts(account_name):
        message_dict = {
            "action": ClientRequestFieldName.GET_CONTACTS.value,
            "time": time.time(),
            "user_login": account_name
        }
        return message_dict

    @staticmethod
    def __create_add_contact(owner_login, contact_login):
        message_dict = {
            "action": ClientRequestFieldName.ADD_CONTACT.value,
            "user_id": owner_login,
            "time": time.time(),
            "user_login": contact_login
        }
        return message_dict

    @staticmethod
    def __create_del_contact(owner_login, contact_login):
        message_dict = {
            "action": ClientRequestFieldName.DEL_CONTACT.value,
            "user_id": owner_login,
            "time": time.time(),
            "user_login": contact_login
        }
        return message_dict

    def logout(self):
        self.__stopped = True
        if self.__receiver:
            self.__receiver.stop()

    def stopped(self) -> bool:
        return self.__stopped

    def await_termination(self, timeout=5):
        if not self.__receiver:
            return
        self.__receiver.join(timeout)
        self.__sock.close()

    def send(self, recipient_name, message, result):
        if self.__sock is None:
            raise ValueError('Client is not initialised')
        self.__task_sender.submit_task(self.__create_message(self.__account, recipient_name, message), result)

    def login(self, login, password, result):
        if self.__connected:
            raise ValueError('Client already connected')
        self.__connected = True
        self.__sock = create_socket()
        self.__sock.connect((self.__address, self.__port))
        response_queue = Queue()

        self.__receiver = ReceiverThread(self.__sock, response_queue, self.__message_listener)
        self.__task_sender = SenderThread(self.__sock, response_queue)
        self.__task_sender.start()
        self.__receiver.start()

        self.__task_sender.submit_task(self.__create_presence_msg(login),
                                       lambda response: self.__login_callback(login, response, result))

    def __login_callback(self, login, response, callback):
        self.__account = login
        callback(response)

    def get_contact_list(self, result):
        self.__task_sender.submit_task(self.__create_get_contacts(self.__account), result)

    def add_contact(self, contact: str, result):
        self.__task_sender.submit_task(self.__create_add_contact(self.__account, contact), result)

    def del_contact(self, contact: str, result):
        self.__task_sender.submit_task(self.__create_del_contact(self.__account, contact), result)


def main():
    client_name = input('Input your name: ')
    client = Client(lambda msg: print(msg), address='localhost', port=7777)
    login_queue = Queue()
    client.login(client_name, "ignored", lambda msg: login_queue.put(msg))

    login_response = login_queue.get()
    while not client.stopped():
        friend = input('Input friend\'s name: ')
        if friend == ':quit':
            break
        while True:
            mes = input('Input your message: ')
            if mes == ':quit':
                break
            client.send(friend, mes,
                        lambda response: logger.info("Message sent to server [response=%s]", response))
    client.await_termination()


if __name__ == '__main__':
    main()
