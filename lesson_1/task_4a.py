"""4. Продолжаем работать над проектом «Мессенджер»:.
a) Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и на запись в него. Уместно использовать
модуль subprocess).
"""
import subprocess

if __name__ == '__main__':
    sender = subprocess.Popen(['python', 'client_sender.py'])
    receiver = subprocess.Popen(['python', 'client_receiver.py'])

    sender.wait()
    receiver.wait()
