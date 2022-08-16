""" Модуль, отображающий основной UI приложения"""

import sys
from datetime import datetime
from PyQt5.QtGui import QStandardItem, QBrush, QColor, QStandardItemModel
from common.messages import ServerResponseFieldName, ResponseCode, ClientRequestFieldName, MessageType, MsgFieldName
from log.client_log_config import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QListWidget, QLineEdit, QDateEdit
from client.client import Client
from client.client_repository import ClientRepository

logger = logging.getLogger('gb.client')


class WelcomeForm(QDialog):
    """
    Класс стартового окна приложения с формой логина и регистрации
    """
    def __init__(self):
        super(WelcomeForm, self).__init__()
        loadUi('welcome_form.ui', self)
        self.loginbtn.clicked.connect(self.go_to_login)
        self.sign_up_btn.clicked.connect(self.sign_up_for_messenger)

    def go_to_login(self):
        """
        Метод-обработчик нажатия кнопки login. Отображает форму логина Проверяет заполненность полей формы.
        """
        login_obj = LoginForm()
        widget.addWidget(login_obj)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sign_up_for_messenger(self):
        """
        Метод-обработчик нажатия кнопки sign_up. Отображает форму регистрации
        """
        registration = SignUpForm()
        widget.addWidget(registration)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginForm(QDialog):
    """
    Класс с формой логина
    """
    login_signal = pyqtSignal(dict)

    def __init__(self):
        super(LoginForm, self).__init__()
        loadUi('login.ui', self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbtn.clicked.connect(self.connect_to_chat)
        self.back_btn.clicked.connect(self.back_to_welcome)
        self.client = Client()
        self.login_signal.connect(self.show_account_form)

    def connect_to_chat(self):
        """
        Метод-обработчик нажатия кнопки login. Проверяет заполненность полей формы
        """
        client_login = self.login_field.text()
        password = self.password_field.text()

        if len(client_login) == 0 or len(password) == 0:
            self.error_field.setText('Please input all fields')
        else:
            try:
                self.client.login(client_login, password, lambda response: self.login_signal.emit(response))
            except ConnectionError:
                self.error_field.setText('Login and password do not match')

    @staticmethod
    def back_to_welcome():
        """
        Метод-обработчик нажатия кнопки back. Возвращает стартовое окно welcome
        """
        welcome_form = WelcomeForm()
        widget.addWidget(welcome_form)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @pyqtSlot(dict)
    def show_account_form(self, response):
        """
        Метод-слот, отображает основную форму приложения пользователя с чатом и списком контактов
        """
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code == ResponseCode.OK.value:
            account = AccountForm(self.client)
            widget.addWidget(account)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif code == 400:
            self.error_field.setText('Login is not signed up')


class SignUpForm(QDialog):
    """
    Класс с формой регистрации
    """
    sign_up_signal = pyqtSignal(dict)

    def __init__(self):
        super(SignUpForm, self).__init__()
        loadUi('sign_up_form.ui', self)
        self.login = self.findChild(QLineEdit, "login_field")
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.name = self.findChild(QLineEdit, "name_field")
        self.surname = self.findChild(QLineEdit, "surname_field")
        self.birthdate = self.findChild(QDateEdit, "birthdate_field")
        self.sign_up_btn.clicked.connect(self.sign_up_for_messenger)
        self.back_btn.clicked.connect(self.back_to_welcome)
        self.client = Client()
        self.sign_up_signal.connect(self.show_account_form)

    def sign_up_for_messenger(self):
        """
        Метод-обработчик нажатия кнопки sign_up. Проверяет заполненность полей формы
        """
        user_login = self.login_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        name = self.name_field.text()
        surname = self.surname_field.text()
        birthdate = self.birthdate_field.text()

        if len(user_login) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(name) == 0 or len(
                surname) == 0:
            self.error_field.setText('Please fill in all inputs')
        elif password != confirm_password:
            self.error_field.setText('Passwords don\'t match, please try again')
        else:
            try:
                self.client.sign_up(user_login, password, name, surname, birthdate,
                                    lambda response: self.sign_up_signal.emit(response))
            except ConnectionError:
                self.error_field.setText('Login and password do not match')

    @pyqtSlot(dict)
    def show_account_form(self, response):
        """
        Метод-слот, отображает основную форму приложения пользователя с чатом и списком контактов
        """
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code == ResponseCode.OK.value:
            account = AccountForm(self.client)
            widget.addWidget(account)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def back_to_welcome(self):
        """
        Метод-обработчик нажатия кнопки back. Возвращает стартовое окно welcome
        """
        welcome_form = WelcomeForm()
        widget.addWidget(welcome_form)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AccountForm(QDialog):
    """
    Класс с основной формой приложения пользователя с чатом и списком контактов
    """
    cont_list_signal = pyqtSignal(dict)
    add_contact_signal = pyqtSignal(str, dict)
    del_contact_signal = pyqtSignal(str, dict)
    message_sent_signal = pyqtSignal(str, str, dict)
    receive_message_signal = pyqtSignal(dict)

    def __init__(self, client: Client):
        super(AccountForm, self).__init__()
        self.selected_contact: str = ""
        self.client = client
        self.database = ClientRepository(f'sqlite:///db-{client.account_name}.sqlite')
        loadUi('account_form.ui', self)
        self.cont_list_signal.connect(self.handle_contacts_response)
        self.contacts_list = self.findChild(QListWidget, "contacts_list")
        client.get_contact_list(lambda response: self.cont_list_signal.emit(response))
        self.contacts_list.doubleClicked.connect(self.set_current_chat)
        self.input_contact_login = self.findChild(QtWidgets.QLineEdit)
        self.input_message = self.findChild(QtWidgets.QTextEdit, "input_message")
        self.chat_list = self.findChild(QtWidgets.QListView, "chat_list")
        self.chat_model = QStandardItemModel()
        self.chat_list.setModel(self.chat_model)
        self.add_contact_signal.connect(self.show_new_contact)
        self.add_contact_btn.clicked.connect(self.add_contact_to_list)
        self.del_contact_signal.connect(self.remove_contact)
        self.delete_contact_btn.clicked.connect(self.del_contact_from_list)
        self.send_btn.clicked.connect(self.send_btn_clicked)
        self.message_sent_signal.connect(self.message_sent)
        self.client.subscribe_to_messages(lambda msg: self.receive_message_signal.emit(msg))
        self.receive_message_signal.connect(self.message_received)

    @pyqtSlot(dict)
    def handle_contacts_response(self, response):
        """
        Метод отображения списка контактов
        """
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code == ResponseCode.ACCEPTED.value:
            contacts = response['alert'].lstrip('"[').rstrip(']"').split(',')
            for contact in map(lambda it: it.strip("'"), contacts):
                self.contacts_list.addItem(contact)
                self.database.add_contact(contact)
            self.database.session.commit()

    def send_btn_clicked(self):
        """
        Метод-обработчик нажатия кнопки send. Отправляет сообщение контакту
        """
        contact = self.input_contact_login.text()
        message = self.input_message.toPlainText()
        if not contact or not message:
            return

        self.client.send(contact, message,
                         lambda response: self.message_sent_signal.emit(contact, message, response))

    @pyqtSlot(str, str, dict)
    def message_sent(self, contact, message, response):
        """
        Метод сохранения отправленного сообщения в базе данных
        """
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code != ResponseCode.OK.value:
            return
        now = datetime.now()
        self.database.save_message(self.client.account_name, contact, message, now)
        self.database.session.commit()
        self.input_message.clear()
        if self.selected_contact != contact:
            return
        self.__add_sent_msg_to_model(now, message)

    def set_current_chat(self):
        """
        Метод установки текущего чата по выделенному элементу в списке контактов
        """
        self.chat_model.removeRows(0, self.chat_model.rowCount())
        contact_login = self.contacts_list.currentItem().text()
        self.selected_contact = contact_login
        data = self.database.get_message_history()
        data.sort(key=lambda x: x.date, reverse=False)
        logger.info('response received %s', data)
        acc_name = self.client.account_name
        for message_history in data:
            if message_history.from_acc == acc_name and message_history.to_acc == self.selected_contact:
                self.__add_sent_msg_to_model(message_history.date, message_history.message)
            elif message_history.to_acc == acc_name and message_history.from_acc == self.selected_contact:
                self.__add_received_msg_to_model(message_history.date, message_history.message)

    def __add_sent_msg_to_model(self, date_time, message):
        """
        Метод отображения отправленного сообщения в текущем чате
        """
        mess = QStandardItem(f'Sent at {date_time.replace(microsecond=0)}:\n {message}')
        mess.setEditable(False)
        mess.setTextAlignment(Qt.AlignRight)
        mess.setBackground(QBrush(QColor(228, 242, 255)))
        self.chat_model.appendRow(mess)

    def __add_received_msg_to_model(self, date_time, message):
        """
        Метод отображения полученного сообщения в текущем чате
        """
        mess = QStandardItem(f'Received at {date_time.replace(microsecond=0)}:\n {message}')
        mess.setEditable(False)
        mess.setBackground(QBrush(QColor(230, 230, 255)))
        mess.setTextAlignment(Qt.AlignLeft)
        self.chat_model.appendRow(mess)

    def add_contact_to_list(self):
        """
        Метод проверки нового контакта в базе данных при добавлении в список контактов
        """
        contact = self.input_contact_login.text()
        if contact:
            if not self.database.check_contact(contact):
                self.client.add_contact(contact, lambda response: self.add_contact_signal.emit(contact, response))
            else:
                self.label_3.setText('This contact is already in your contact list')

    @pyqtSlot(str, dict)
    def show_new_contact(self, contact, response):
        """
        Метод добавления контакта в список контактов
        """
        if response.get(ServerResponseFieldName.RESPONSE.value) == ResponseCode.OK.value:
            self.contacts_list.addItem(contact)
            self.database.add_contact(contact)
            self.database.session.commit()
        if response.get(ServerResponseFieldName.RESPONSE.value) == ResponseCode.BAD_REQUEST.value:
            self.label_3.setText('This contact is absent in messenger')

    @pyqtSlot(dict)
    def message_received(self, msg):
        """
        Метод сохранения полученного сообщения в базу данных
        """
        if not msg or not msg.get(ClientRequestFieldName.ACTION) != MessageType.MESSAGE:
            return

        if msg.get(MsgFieldName.TO.value) != self.client.account_name:
            return

        contact = msg.get(MsgFieldName.FROM.value)
        message = msg.get(MsgFieldName.MESSAGE.value)
        time = msg.get(MsgFieldName.TIME.value)

        if not contact or not message:
            return
        time = datetime.now() if not time else datetime.fromtimestamp(time)
        self.database.save_message(contact, self.client.account_name, message, time)
        self.database.session.commit()

        if self.selected_contact != contact:
            return
        self.__add_received_msg_to_model(time, message)

    def del_contact_from_list(self):
        contact = self.input_contact_login.text()
        if contact:
            if self.database.check_contact(contact):
                self.client.del_contact(contact, lambda response: self.del_contact_signal.emit(contact, response))
                return
            self.label_3.setText('This login is absent in your contact list')

    @pyqtSlot(str, dict)
    def remove_contact(self, contact, response):
        """
        Метод-обработчик для удаления контакта
        """
        if response.get(ServerResponseFieldName.RESPONSE.value) == ResponseCode.OK.value:
            index = -1
            for i in range(self.contacts_list.count()):
                if self.contacts_list.item(i).text() == contact:
                    index = i
                    break
            if index < 0:
                return
            self.contacts_list.takeItem(index)
            self.database.del_contact(contact)
            self.database.session.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome_obj = WelcomeForm()
    widget = QStackedWidget()
    widget.addWidget(welcome_obj)
    widget.setFixedSize(901, 681)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')
