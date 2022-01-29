"""
2.Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только последний
октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.
"""
from ipaddress import ip_address

from task_1 import host_ping


def host_range_ping(first_address: str, number: int) -> (list, list):
    if not isinstance(number, int):
        raise ValueError("number is not an int")
    if number <= 0:
        raise ValueError('number is less or equal 0')

    first_address_ip = ip_address(first_address)
    last_oct = int(first_address_ip) % 256
    iterations = min(255 - last_oct, number)

    address_list = [str(first_address_ip + item) for item in range(iterations)]
    return host_ping(address_list)


if __name__ == '__main__':
    while True:
        start_ip = input("Input first address: ")
        number = int(input('Input ip hosts count: '))  # сколько хостов хотите проверить
        try:
            reachable, unreachable = host_range_ping(start_ip, number)
            for addresses in reachable:
                print(f"Host is reachable {addresses}")
            for addresses in unreachable:
                print(f"Host is unreachable {addresses}")
        except ValueError as e:
            print(f"Unable to ping ip range {e}")
