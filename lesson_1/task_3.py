"""
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2. Но в данном случае
результат должен быть итоговым по всем ip-адресам, представленным в табличном формате из двух столбцов: reachable и
unreachable(использовать модуль tabulate)
"""

from tabulate import tabulate
from task_2 import host_range_ping


def host_range_ping_tab(first_address, ip_count):
    reachable, unreachable = host_range_ping(first_address, ip_count)

    # Option 1
    print(tabulate({
        'Reachable': reachable,
        'Unreachable': unreachable
    }, headers='keys'))

    # Option 2
    rows = []
    r_len = len(reachable)
    u_len = len(unreachable)
    for i in range(max(r_len, u_len)):
        right = None
        left = None
        if i < r_len:
            left = reachable[i]
        if i < u_len:
            right = unreachable[i]
        rows.append((left, right))

    print(tabulate(rows, headers=["Reachable", "Unreachable"]))


if __name__ == '__main__':
    while True:
        start_ip = input("Input first address: ")
        number = int(input('Input ip hosts count: '))  # сколько хостов хотите проверить
        try:
            host_range_ping_tab(start_ip, number)
        except ValueError as e:
            print(f"Unable to ping ip range {e}")
