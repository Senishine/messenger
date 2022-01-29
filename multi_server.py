import queue
import select
from socket import socket, AF_INET, SOCK_STREAM

from log.server_log_config import logging
from messages import MessageType, ClientRequestFieldName, PresenceFieldName, MsgFieldName, ResponseCode, \
    ServerResponseFieldName
from utils import send_message, get_data

logger = logging.getLogger('gb.server')


def validate_presence(msg) -> str:
    if not msg:
        return "Empty message"
    if msg.get(ClientRequestFieldName.ACTION.value) != MessageType.PRESENCE.value:
        return f"Message type is not {MessageType.PRESENCE.value}"
    if not msg.get(PresenceFieldName.USER.value) or \
            not msg.get(PresenceFieldName.USER.value).get(PresenceFieldName.ACCOUNT.value):
        return "Account name not filled"
    return ""


def validate_msg(msg, account) -> str:
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


def create_response(code=200, msg=None):
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


def remove_if_present(key, d: dict):
    value = d.get(key)
    if value is not None:
        del d[key]


def remove_from_list(obj, l: list):
    try:
        l.remove(obj)
    except ValueError:
        pass


def start_server(address='', port=7777):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)
    s.setblocking(False)
    input_sockets = [s]  # sockets which should be checked for available data to read (на готовность к вводу)
    output_sockets = []  # sockets which should be checked for readiness to write data (проверяются на готовность к выводу)

    # when online only
    s_to_account = {}
    account_to_s = {}
    # ~ when online only

    account_to_messages = {}
    s_to_error_msgs = {}

    def handle_error(s, err_code, err_msg):
        if s_to_error_msgs.get(s):
            return
        s_to_error_msgs[s] = create_response(err_code, err_msg)
        remove_from_list(s, input_sockets)

    def handle_writable_socket(s: socket):
        try:
            socket_error = s_to_error_msgs.get(s)
            if socket_error is not None:
                send_message(socket_error, s)
                cleanup_socket(s)
                return
            account = s_to_account.get(s)
            if not account:
                # no account association -> presence not sent yet
                return
            queue = account_to_messages.get(account)
            if not queue or queue.empty():
                return
            message = queue.get_nowait()
            send_message(message, s)
        except ConnectionError as e:
            logger.warning('Error occurred on client socket during sending data. Socket=%s, error=%s', sck, e)
            cleanup_socket(sck)

    def handle_message_from_client(s: socket):
        try:
            err_message = s_to_error_msgs.get(s)
            if err_message is not None:
                return
            try:
                msg = get_data(s)
            except ValueError:
                handle_error(s, ResponseCode.BAD_REQUEST.value, 'Invalid JSON')
                return
            msg_type = msg.get(ClientRequestFieldName.ACTION.value)
            if msg_type == MessageType.PRESENCE.value:
                err_msg = validate_presence(msg)
                if err_msg:
                    handle_error(s, ResponseCode.BAD_REQUEST.value, err_msg)
                    return
                if s_to_account.get(s):
                    handle_error(s, ResponseCode.CONFLICT.value, 'Connection with this login already exists')
                    return
                else:
                    account: str = msg[PresenceFieldName.USER.value][PresenceFieldName.ACCOUNT.value]
                    s_to_account[s] = account
                    account_to_s[account] = s
            elif msg_type == MessageType.MESSAGE.value:
                account = s_to_account.get(s)
                if not account:
                    handle_error(s, ResponseCode.UNAUTHORIZED.value, 'No presence message received')
                    return
                err_msg = validate_msg(msg, account)
                if err_msg:
                    handle_error(s, ResponseCode.BAD_REQUEST.value, err_msg)
                    return
                to = msg[MsgFieldName.TO.value]
                account_to_messages.setdefault(to, queue.Queue()).put(msg)
                return
            else:
                handle_error(s, ResponseCode.BAD_REQUEST.value, 'Unsupported message type')
                return
        except ConnectionError as e:
            logger.warning('Error occurred on client socket during receiving data. Socket=%s, error=%s', sck, e)
            cleanup_socket(sck)
        except Exception as e:
            logger.error("Unexpected error during client message handling %s", e)
            handle_error(s, ResponseCode.INTERNAL_SERVER_ERROR.value, 'Server error')

    def cleanup_socket(sck):
        account = s_to_account.get(sck)
        if account is not None:
            remove_if_present(account, account_to_s)
        remove_if_present(sck, s_to_account)
        remove_if_present(sck, s_to_error_msgs)

        remove_from_list(sck, input_sockets)
        remove_from_list(sck, output_sockets)

        logger.info('Socket %s was closed, remaining: input=%s, output=%s, accounts=%s, error_sockets=%s',
                    sck, len(input_sockets), len(output_sockets), account_to_s.keys(), len(s_to_error_msgs))
        sck.close()

    while input_sockets:
        r_list, w_list, ex_list = select.select(input_sockets, output_sockets, input_sockets)
        # This call will block the program (unless a timeout argument is passed) until some of the passed sockets are ready.
        # In this moment, the call will return three lists with sockets for specified operations.
        for sck in r_list:
            if sck is s:
                client, addr = s.accept()
                logger.info('Accepted client connection [client_address=%s]', addr)
                client.setblocking(False)
                input_sockets.append(client)
                output_sockets.append(client)
            else:
                handle_message_from_client(sck)

        for sck in w_list:
            handle_writable_socket(sck)

        for sck in ex_list:
            cleanup_socket(sck)


if __name__ == '__main__':
    start_server()
