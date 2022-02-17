# *В следующем уроке мы будем изучать дескрипторы и метаклассы.
# Но вы уже сейчас можете перевести часть кода из функционального стиля в объектно-ориентированный.
# Создайте классы «Клиент» и «Сервер», а используемые функции превратите в методы классов.
import hashlib
import hmac
import os
import queue
import select
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

from sqlalchemy.exc import DatabaseError

from repository import Repository
from common.descriptor import Port
from log.server_log_config import logging
from common.messages import MessageType, ClientRequestFieldName, UserFieldName, MsgFieldName, ResponseCode, \
    RequestToServer, AuthenticateFieldName
from common.utils import send_message, get_data
from common.verifiers import ServerVerifier
from server.server_utils import remove_if_present, validate_get_contact, validate_del_contact, validate_add_contact, \
    validate_user_msg, validate_authenticate, validate_sign_up, validate_presence, remove_from_list, create_response
from server.utils import get_config

logger = logging.getLogger('gb.server')


class Request:
    def __init__(self, sock: socket, msg: dict):
        self.sock: socket = sock
        self.msg: dict = msg
        self.account = None


def login_required(method):
    def wrapper(self, request):
        owner_account = self._s_to_account.get(request.sock)
        if not owner_account:
            self.__handle_error(request.sock, ResponseCode.UNAUTHORIZED.value, 'No presence message received')
            return
        request.account = owner_account
        method(self, request)

    return wrapper


class Server(metaclass=ServerVerifier):
    __port = Port(logger)

    def __init__(self, db_url, address='', port=7777):
        self.__handlers = {
            MessageType.AUTHENTICATE.value: self.__handle_authenticate_msg,
            MessageType.PRESENCE.value: self.__handle_presence_msg,
            MessageType.SIGN_UP.value: self.__handle_sign_up_msg,
            MessageType.MESSAGE.value: self.__handle_user_msg,
            MessageType.GET_CONTACTS.value: self.__handle_get_contact_msg,
            MessageType.ADD_CONTACT.value: self.__handle_add_contact_msg,
            MessageType.DEL_CONTACT.value: self.__handle_del_contact_msg
        }
        self.__address = address
        self.__port = port
        self.__started = False
        self.__input_sockets = []  # sockets which should be checked for available data to read (на готовность к вводу)
        self.__output_sockets = []  # sockets which should be checked for readiness to write data (проверяются на готовность к выводу)
        # when online only
        self._s_to_account = {}
        self.__account_to_s = {}
        # ~ when online only
        self.__account_to_messages = {}
        self.__socket_to_messages = {}
        self.__s_to_addr = {}
        self.__s_to_error_msgs = {}
        self.db = Repository(db_url)

    def __send_response_to_socket(self, sock, code, msg=None):
        self.__socket_to_messages.setdefault(sock, queue.Queue()) \
            .put(create_response(code, msg))

    def __send_response(self, account, code, msg=None):
        self.__account_to_messages.setdefault(account, queue.Queue()) \
            .put(create_response(code, msg))

    def __handle_error(self, s, err_code, err_msg):
        if self.__s_to_error_msgs.get(s):
            return
        self.__s_to_error_msgs[s] = create_response(err_code, err_msg)
        remove_from_list(s, self.__input_sockets)

    def __handle_writable_socket(self, s: socket):
        try:
            socket_error = self.__s_to_error_msgs.get(s)
            if socket_error is not None:
                send_message(socket_error, s)
                self.__cleanup_socket(s)
                return

            messages = self.__socket_to_messages.get(s)
            if messages and not messages.empty():
                message = messages.get_nowait()
                logger.debug('Sending message to socket [socket=%s, message=%s]', s, message)
                send_message(message, s)

            account = self._s_to_account.get(s)
            if not account:
                # no account association -> presence not sent yet
                return
            msg_queue = self.__account_to_messages.get(account)
            if not msg_queue or msg_queue.empty():
                return
            message = msg_queue.get_nowait()
            logger.debug('Sending message to user [login=%s, message=%s]', account, message)
            send_message(message, s)
        except ConnectionError as e:
            logger.warning('Error occurred on client socket during sending data. Socket=%s, error=%s', s, e)
            self.__cleanup_socket(s)

    def __handle_presence_msg(self, request):
        err_msg = validate_presence(request.msg)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        if self._s_to_account.get(request.sock):
            self.__handle_error(request.sock, ResponseCode.CONFLICT.value,
                                'Connection with this login is already exists')
            return
        else:
            account: str = request.msg[UserFieldName.USER.value][UserFieldName.ACCOUNT.value]
            self.__send_response(account, ResponseCode.OK.value)

    def __handle_sign_up_msg(self, request):
        err_msg = validate_sign_up(request.msg)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        elif self._s_to_account.get(request.sock):
            self.__handle_error(request.sock, ResponseCode.CONFLICT.value,
                                'Connection with this login is already exists')
            return
        login: str = request.msg.get(UserFieldName.USER.value).get(UserFieldName.LOGIN.value)
        password = request.msg.get(UserFieldName.USER.value).get(AuthenticateFieldName.PASSWORD.value)
        name = request.msg.get(UserFieldName.USER.value).get(UserFieldName.NAME.value)
        surname = request.msg.get(UserFieldName.USER.value).get(UserFieldName.SURNAME.value)
        birthdate = request.msg.get(UserFieldName.USER.value).get(UserFieldName.BIRTHDATE.value)
        user = None
        try:
            user = self.db.get_user(login)
        except DatabaseError:
            pass
        if user is not None:
            self.__send_response(login, ResponseCode.BAD_REQUEST.value, 'Account with this login is already signed up')
            return
        logger.info('Login is checked [login=%s], sign up beginning', login)
        salt = os.urandom(16)
        hash_str = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.db.sign_up(login, name, surname, hash_str, salt, birthdate)
        self.db.add_history(Repository.UserHistory(login, datetime.now(), self.__s_to_addr[request.sock][0]))
        self._s_to_account[request.sock] = login
        self.__account_to_s[login] = request.sock
        self.__send_response(login, ResponseCode.OK.value)
        logger.info('Login is signed up [login=%s]', login)

    def __handle_authenticate_msg(self, request):
        err_msg = validate_authenticate(request.msg)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        elif self._s_to_account.get(request.sock):
            self.__handle_error(request.sock, ResponseCode.CONFLICT.value,
                                'Connection with this login is already exists')
            return
        account: str = request.msg.get(UserFieldName.USER.value).get(UserFieldName.ACCOUNT.value)
        client_pass = request.msg.get(UserFieldName.USER.value).get(AuthenticateFieldName.PASSWORD.value)
        user = None
        try:
            user = self.db.get_user(account)
        except DatabaseError:
            pass
        if user is None:
            self.__send_response(account, ResponseCode.UNAUTHORIZED.value, 'User does not exist')
            return

        logger.info('Login is checked [login=%s], checking pass', account)
        salt = user.salt
        hash_str = hashlib.pbkdf2_hmac('sha256', client_pass.encode('utf-8'), salt, 100000)
        if hmac.compare_digest(hash_str, self.db.get_hash(account)):
            self.db.add_history(Repository.UserHistory(account, datetime.now(), self.__s_to_addr[request.sock][0]))
            self._s_to_account[request.sock] = account
            self.__account_to_s[account] = request.sock
            self.__send_response(account, ResponseCode.OK.value)
        else:
            logger.debug('The user [login=%s] inputted incorrect password', account)
            self.__send_response_to_socket(request.sock, ResponseCode.BAD_REQUEST.value, 'Password is incorrect')

    @login_required
    def __handle_user_msg(self, request):
        err_msg = validate_user_msg(request.msg, request.account)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        to = request.msg[MsgFieldName.TO.value]
        self.__account_to_messages.setdefault(to, queue.Queue()).put(request.msg)
        self.__send_response(request.account, ResponseCode.OK.value)

    @login_required
    def __handle_add_contact_msg(self, request):
        err_msg = validate_add_contact(request.msg, request.account)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        owner: str = request.msg.get(RequestToServer.USER_ID.value)
        contact_login = request.msg.get(RequestToServer.USER_LOGIN.value)
        try:
            self.db.add_contact(owner, contact_login)
            self.__send_response(owner, ResponseCode.OK.value)
        except DatabaseError:
            self.__send_response(owner, ResponseCode.BAD_REQUEST.value, 'Invalid contact name')

    @login_required
    def __handle_del_contact_msg(self, request):
        err_msg = validate_del_contact(request.msg, request.account)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        owner: str = request.msg.get(RequestToServer.USER_ID.value)
        contact_login = request.msg.get(RequestToServer.USER_LOGIN.value)
        try:
            self.db.del_contact(owner, contact_login)
            self.__send_response(owner, ResponseCode.OK.value)
        except DatabaseError:
            self.__send_response(owner, ResponseCode.BAD_REQUEST.value, 'Invalid contact name')

    @login_required
    def __handle_get_contact_msg(self, request):
        err_msg = validate_get_contact(request.msg, request.account)
        if err_msg:
            self.__handle_error(request.sock, ResponseCode.BAD_REQUEST.value, err_msg)
            return
        owner: str = request.msg.get(RequestToServer.USER_LOGIN.value)
        contacts = self.db.get_contacts(owner)
        converted = map(lambda it: "\'" + str(it[0]) + "\'", contacts)
        self.__send_response(owner, ResponseCode.ACCEPTED.value, f"[{','.join(converted)}]")

    def __handle_message_from_client(self, s: socket):
        try:
            err_message = self.__s_to_error_msgs.get(s)
            if err_message is not None:
                return
            try:
                msg = get_data(s)
                logger.debug("Received message from client [msg=%s]", msg)
            except ValueError:
                self.__handle_error(s, ResponseCode.BAD_REQUEST.value, 'Invalid JSON')
                return

            msg_type = msg.get(ClientRequestFieldName.ACTION.value)
            request = Request(s, msg)
            handler = self.__handlers.setdefault(
                msg_type,
                lambda r: self.__handle_error(r.sock,
                                              ResponseCode.BAD_REQUEST.value,
                                              'Unsupported message type')
            )
            handler(request)
        except ConnectionError as e:
            logger.warning('Error occurred on client socket during receiving data. Socket=%s, error=%s', s, e)
            self.__cleanup_socket(s)
        except Exception as e:
            logger.error("Unexpected error during client message handling %s", e)
            self.__handle_error(s, ResponseCode.INTERNAL_SERVER_ERROR.value, 'Server error')

    def __cleanup_socket(self, sck):
        account = self._s_to_account.get(sck)
        if account is not None:
            remove_if_present(account, self.__account_to_s)
        remove_if_present(sck, self._s_to_account)
        remove_if_present(sck, self.__socket_to_messages)
        remove_if_present(sck, self.__s_to_addr)
        remove_if_present(sck, self.__s_to_error_msgs)

        remove_from_list(sck, self.__input_sockets)
        remove_from_list(sck, self.__output_sockets)

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
            # This call will block the program (unless a timeout argument is passed)
            # until some of the passed sockets are ready.
            # In this moment, the call will return three lists with sockets for specified operations.
            for sck in r_list:
                if sck is s:
                    client, addr = s.accept()
                    logger.info('Accepted client connection [client_address=%s]', addr)
                    client.setblocking(False)
                    self.__input_sockets.append(client)
                    self.__output_sockets.append(client)
                    self.__s_to_addr[client] = addr
                else:
                    self.__handle_message_from_client(sck)

            for sck in w_list:
                self.__handle_writable_socket(sck)

            for sck in ex_list:
                self.__cleanup_socket(sck)


if __name__ == '__main__':
    config = get_config()
    settings = config['SETTINGS']
    server = Server(settings['database_url'], settings['listen_address'], int(settings['port']))
    server.start()
