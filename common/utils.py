"""Утилиты"""

import json

DEFAULT_ENCODING = 'utf-8'


def send_message(message, sock):
    """
    Функция кодирования и отправки сообщения
    принимает словарь и отправляет его
    """
    if isinstance(message, str):
        data_to_send = message.encode(DEFAULT_ENCODING)
    elif isinstance(message, dict):
        data_to_send = json.dumps(message).encode(DEFAULT_ENCODING)  # serialize in json
    elif isinstance(message, bytes):
        data_to_send = message
    else:
        raise ValueError('unsupported type of message')
    sock.send(data_to_send)


def get_data(sock) -> dict:
    """
    Функция приёма и декодирования сообщения
    принимает байты, выдаёт словарь
    """
    data = sock.recv(640)
    return json.loads(data.decode(DEFAULT_ENCODING))
