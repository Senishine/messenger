"""4. Продолжаем работать над проектом «Мессенджер»:.
b) Реализовать скрипт, запускающий указанное количество клиентских приложений.
"""
import subprocess

if __name__ == '__main__':
    s_num = int(input('Input sender\'s count: '))
    r_num = int(input('Input receiver\'s count: '))

    senders = []
    receivers = []

    for i in range(s_num):
        senders.append(subprocess.Popen(['python', 'client_sender.py']))
    for i in range(r_num):
        receivers.append(subprocess.Popen(['python', 'client_receiver.py']))

    for s in senders:
        s.wait()

    for r in receivers:
        r.wait()
