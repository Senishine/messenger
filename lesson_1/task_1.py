"""
 Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""
from ipaddress import ip_address
import subprocess, socket


def host_ping(lst) -> (list, list):
    reachable = []
    unreachable = []
    for addr in lst:
        try:
            addr = ip_address(socket.gethostbyname(addr))
        except ValueError as e:
            print(f'The address {addr} is not valid IP address')

        code = subprocess.call(["ping", str(addr), '-n', '2', '-w', '200'], stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL)
        if code == 0:
            reachable.append(addr)
        else:
            unreachable.append(addr)
    return (reachable, unreachable)


if __name__ == '__main__':
    addresses = ['google.com', 'vk.com', '192.168.15.22', '222.33.33.2']
    reachable, unreachable = host_ping(addresses)
    for addresses in reachable:
        print(f"Host is reachable {addresses}")
    for addresses in unreachable:
        print(f"Host is unreachable {addresses}")
