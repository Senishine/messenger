import dis


class ClientVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError(f'Used restricted method [method={command}]')
        if 'send_message' not in methods:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)


class ServerVerifier(type):
    def __init__(cls, clsname, bases, clsdict):
        found_socket = False
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                expected_ipv4_attr = ['SOCK_STREAM', 'AF_INET']
                for i in ret:
                    if found_socket and len(expected_ipv4_attr) > 0:
                        if i.opname != 'LOAD_GLOBAL' or i.argval != expected_ipv4_attr.pop():
                            raise TypeError('Invalid socket initialisation, expected: socket(AF_INET, SOCK_STREAM)')
                        continue
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval == 'socket':
                            found_socket = True
                    elif i.opname == 'LOAD_METHOD' and i.argval == 'connect':
                        raise TypeError('Used restricted function "connect"')

        if not found_socket:
            raise TypeError('Server socket has not been initialised')
        super().__init__(clsname, bases, clsdict)
