""" Реализовать обработку нескольких клиентов на сервере, используя функцию select. Клиенты должны общаться
в «общем чате»: каждое сообщение участника отправляется всем, подключенным к серверу.
"""
import logging
import queue
import select
from socket import socket, AF_INET, SOCK_STREAM


def start_server(address='', port=7777):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)
    s.setblocking(False)
    input_sockets = [s]  # sockets which should be checked for available data to read (на готовность к вводу)
    output_sockets = []  # sockets which should be checked for readiness to write data (проверяются на готовность к выводу)
    messages = {}

    def cleanup_socket(sck):
        input_sockets.remove(sck)
        output_sockets.remove(sck)
        del messages[sck]
        logging.info('Socket %s was closed, remaining: input=%s, output=%s, messages=%s',
                     sck, len(input_sockets), len(output_sockets), messages.keys())
        sck.close()

    while input_sockets:
        r_list, w_list, ex_list = select.select(input_sockets, output_sockets, input_sockets)
        # This call will block the program (unless a timeout argument is passed) until some of the passed sockets are ready.
        # In this moment, the call will return three lists with sockets for specified operations.
        for sck in r_list:
            if sck is s:
                client, addr = s.accept()
                logging.info('Accepted client connection [client_address=%s]', addr)
                client.setblocking(False)
                input_sockets.append(client)
                output_sockets.append(client)
                messages[client] = queue.Queue()
            else:
                try:
                    message = sck.recv(1024)
                    for value in messages.values():  # value - queue of outgoing messages
                        value.put(message)
                except ConnectionError as e:
                    logging.warning('Error occurred on client socket during receiving data. Socket=%s, error=%s', sck,
                                    e)
                    cleanup_socket(sck)

        for sck in w_list:
            val = messages.get(sck)
            if not val or val.empty():
                continue
            message = val.get_nowait()
            try:
                sck.send(message)
            except ConnectionError as e:
                logging.warning('Error occurred on client socket during sending data. Socket=%s, error=%s', sck, e)
                cleanup_socket(sck)

        for sck in ex_list:
            cleanup_socket(sck)


if __name__ == '__main__':
    start_server()
