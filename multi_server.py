# *В следующем уроке мы будем изучать дескрипторы и метаклассы.
# Но вы уже сейчас можете перевести часть кода из функционального стиля в объектно-ориентированный.
# Создайте классы «Клиент» и «Сервер», а используемые функции превратите в методы классов.
import queue
import select
from socket import socket, AF_INET, SOCK_STREAM

from descriptor import Port
from log.server_log_config import logging
from messages import MessageType, ClientRequestFieldName, PresenceFieldName, MsgFieldName, ResponseCode, \
    ServerResponseFieldName
from utils import send_message, get_data
from verifiers import ServerVerifier

logger = logging.getLogger('gb.server')


class Server(metaclass=ServerVerifier):
    __port = Port(logger)

    def __init__(self, address='', port=7777):
        self.__address = address
        self.__port = port
        self.__started = False
        self.__input_sockets = []  # sockets which should be checked for available data to read (на готовность к вводу)
        self.__output_sockets = []  # sockets which should be checked for readiness to write data (проверяются на готовность к выводу)
        # when online only
        self.__s_to_account = {}
        self.__account_to_s = {}
        # ~ when online only
        self.__account_to_messages = {}
        self.__s_to_error_msgs = {}

    @staticmethod
    def __validate_presence(msg) -> str:
        if not msg:
            return "Empty message"
        if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.PRESENCE.value:
            return f"Message type is not {MessageType.PRESENCE.value}"
        if not msg.get(PresenceFieldName.USER.value) or \
                not msg.get(PresenceFieldName.USER.value).get(PresenceFieldName.ACCOUNT.value):
            return "Account name not filled"
        return ""

    @staticmethod
    def __validate_msg(msg, account) -> str:
        if not msg:
            return "Empty message"
        if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.MESSAGE.value:
            return f"Message type is not {MessageType.MESSAGE.value}"
        if not msg.get(MsgFieldName.TO.value):
            return "No 'to' field"
        if not msg.get(MsgFieldName.MESSAGE.value):
            return "No 'message' field"
        if msg.get(MsgFieldName.FROM.value) != account:
            return "'From' field not equal logged in user"
        return ""

    @staticmethod
    def __create_response(code=200, msg=None):
        logger.info('Creating response for client [code=%s, msg=%s]', code, msg)
        assert isinstance(code, int), 'code is not an integer'
        data = {
            ServerResponseFieldName.RESPONSE.value: code
        }

        if msg is None:
            return data
        if 400 <= code <= 600:
            data[ServerResponseFieldName.ERROR.value] = msg
        else:
            data[ServerResponseFieldName.ALERT.value] = msg

        return data

    @staticmethod
    def __remove_if_present(key, d: dict):
        value = d.get(key)
        if value is not None:
            del d[key]

    @staticmethod
    def __remove_from_list(obj, l: list):
        try:
            l.remove(obj)
        except ValueError:
            pass

    def __handle_error(self, s, err_code, err_msg):
        if self.__s_to_error_msgs.get(s):
            return
        self.__s_to_error_msgs[s] = Server.__create_response(err_code, err_msg)
        Server.__remove_from_list(s, self.__input_sockets)

    def __handle_writable_socket(self, s: socket):
        try:
            socket_error = self.__s_to_error_msgs.get(s)
            if socket_error is not None:
                send_message(socket_error, s)
                self.__cleanup_socket(s)
                return
            account = self.__s_to_account.get(s)
            if not account:
                # no account association -> presence not sent yet
                return
            queue = self.__account_to_messages.get(account)
            if not queue or queue.empty():
                return
            message = queue.get_nowait()
            send_message(message, s)
        except ConnectionError as e:
            logger.warning('Error occurred on client socket during sending data. Socket=%s, error=%s', s, e)
            self.__cleanup_socket(s)

    def __handle_message_from_client(self, s: socket):
        try:
            err_message = self.__s_to_error_msgs.get(s)
            if err_message is not None:
                return
            try:
                msg = get_data(s)
            except ValueError:
                self.__handle_error(s, ResponseCode.BAD_REQUEST.value, 'Invalid JSON')
                return
            msg_type = msg.get(ClientRequestFieldName.ACTION.value)
            if msg_type == MessageType.PRESENCE.value:
                err_msg = Server.__validate_presence(msg)
                if err_msg:
                    self.__handle_error(s, ResponseCode.BAD_REQUEST.value, err_msg)
                    return
                if self.__s_to_account.get(s):
                    self.__handle_error(s, ResponseCode.CONFLICT.value, 'Connection with this login already exists')
                    return
                else:
                    account: str = msg[PresenceFieldName.USER.value][PresenceFieldName.ACCOUNT.value]
                    self.__s_to_account[s] = account
                    self.__account_to_s[account] = s
            elif msg_type == MessageType.MESSAGE.value:
                account = self.__s_to_account.get(s)
                if not account:
                    self.__handle_error(s, ResponseCode.UNAUTHORIZED.value, 'No presence message received')
                    return
                err_msg = Server.__validate_msg(msg, account)
                if err_msg:
                    self.__handle_error(s, ResponseCode.BAD_REQUEST.value, err_msg)
                    return
                to = msg[MsgFieldName.TO.value]
                self.__account_to_messages.setdefault(to, queue.Queue()).put(msg)
                return
            else:
                self.__handle_error(s, ResponseCode.BAD_REQUEST.value, 'Unsupported message type')
                return
        except ConnectionError as e:
            logger.warning('Error occurred on client socket during receiving data. Socket=%s, error=%s', s, e)
            self.__cleanup_socket(s)
        except Exception as e:
            logger.error("Unexpected error during client message handling %s", e)
            self.__handle_error(s, ResponseCode.INTERNAL_SERVER_ERROR.value, 'Server error')

    def __cleanup_socket(self, sck):
        account = self.__s_to_account.get(sck)
        if account is not None:
            Server.__remove_if_present(account, self.__account_to_s)
        Server.__remove_if_present(sck, self.__s_to_account)
        Server.__remove_if_present(sck, self.__s_to_error_msgs)

        Server.__remove_from_list(sck, self.__input_sockets)
        Server.__remove_from_list(sck, self.__output_sockets)

        logger.info('Socket %s was closed, remaining: input=%s, output=%s, accounts=%s, error_sockets=%s',
                    sck, len(self.__input_sockets), len(self.__output_sockets),
                    self.__account_to_s.keys(), len(self.__s_to_error_msgs))
        sck.close()

    def start(self):
        if self.__started:
            raise ValueError('Server already started')
        self.__started = True

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.__address, self.__port))
        s.listen(5)
        s.setblocking(False)
        self.__input_sockets.append(s)

        while self.__input_sockets:
            r_list, w_list, ex_list = select.select(self.__input_sockets,
                                                    self.__output_sockets,
                                                    self.__input_sockets)
            # This call will block the program (unless a timeout argument is passed) until some of the passed sockets are ready.
            # In this moment, the call will return three lists with sockets for specified operations.
            for sck in r_list:
                if sck is s:
                    client, addr = s.accept()
                    logger.info('Accepted client connection [client_address=%s]', addr)
                    client.setblocking(False)
                    self.__input_sockets.append(client)
                    self.__output_sockets.append(client)
                else:
                    self.__handle_message_from_client(sck)

            for sck in w_list:
                self.__handle_writable_socket(sck)

            for sck in ex_list:
                self.__cleanup_socket(sck)


if __name__ == '__main__':
    server = Server()
    server.start()
