import sys
from datetime import datetime

from PyQt5.QtGui import QStandardItem, QBrush, QColor, QStandardItemModel

from common.messages import ServerResponseFieldName, ResponseCode
from log.client_log_config import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
# from PyQt5.QtGui import QBrush, QColor, QStandardItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QListWidget, QWidget, QTextEdit, QLineEdit
from client.client import Client
from client.client_repository import ClientRepository

logger = logging.getLogger('gb.client')


class WelcomeForm(QDialog):
    def __init__(self):
        super(WelcomeForm, self).__init__()
        loadUi('welcome_form.ui', self)
        self.loginbtn.clicked.connect(self.go_to_login)
        self.sign_up_btn.clicked.connect(self.sign_up_for_messenger)

    def go_to_login(self):
        login_obj = LoginForm()
        widget.addWidget(login_obj)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sign_up_for_messenger(self):
        registration = SignUpForm()
        widget.addWidget(registration)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginForm(QDialog):
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
        client_login = self.login_field.text()
        password = self.password_field.text()

        if len(client_login) == 0 or len(password) == 0:
            self.error_field.setText('Please input all fields')
        else:
            try:
                self.client.login(client_login, password, lambda response: self.login_signal.emit(response))
            except ConnectionError:
                self.error_field.setText('Unable to contact server')

    @staticmethod
    def back_to_welcome():
        welcome_form = WelcomeForm()
        widget.addWidget(welcome_form)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @pyqtSlot(dict)
    def show_account_form(self, response):
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code == ResponseCode.OK.value:
            account = AccountForm(self.client)
            widget.addWidget(account)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class SignUpForm(QDialog):
    def __init__(self):
        super(SignUpForm, self).__init__()
        loadUi('sign_up_form.ui', self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.sign_up_btn.clicked.connect(self.sign_up_for_messenger)
        self.back_btn.clicked.connect(self.back_to_welcome)

    def sign_up_for_messenger(self):
        user_login = self.login_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        name = self.name_field.text()
        surname = self.surname_field.text()

        if len(user_login) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(name) == 0 or len(
                surname) == 0:
            self.error_field.setText('Please fill in all inputs')
        elif password != confirm_password:
            self.error_field.setText('Password don\'t match, please try again')
        else:
            account = AccountForm(user_login)
            widget.addWidget(account)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def back_to_welcome(self):
        welcome_form = WelcomeForm()
        widget.addWidget(welcome_form)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AccountForm(QDialog):
    cont_list_signal = pyqtSignal(dict)
    add_contact_signal = pyqtSignal(str, dict)
    del_contact_signal = pyqtSignal(str, dict)
    message_sent_signal = pyqtSignal(str, str, dict)

    def __init__(self, client: Client):
        super(AccountForm, self).__init__()
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

    @pyqtSlot(dict)
    def handle_contacts_response(self, response):
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code == ResponseCode.ACCEPTED.value:
            contacts = response['alert'].lstrip('"[').rstrip(']"').split(',')
            for contact in map(lambda it: it.strip("'"), contacts):
                self.contacts_list.addItem(contact)
                self.database.add_contact(contact)
            self.database.session.commit()

    def send_btn_clicked(self):
        contact = self.input_contact_login.text()
        message = self.input_message.toPlainText()
        if not contact or not message:
            return

        self.client.send(contact, message,
                         lambda response: self.message_sent_signal.emit(contact, message, response))

    @pyqtSlot(str, str, dict)
    def message_sent(self, contact, message, response):
        code = response.get(ServerResponseFieldName.RESPONSE.value)
        if code != ResponseCode.OK.value:
            return
        now = datetime.now()
        self.database.save_message(contact, message, now)
        self.database.session.commit()
        contact_login = self.contacts_list.currentItem().text()
        if contact_login != contact:
            return
        self.__add_sent_msg_to_model(now, message)

    def set_current_chat(self):
        self.chat_model.clear()
        contact_login = self.contacts_list.currentItem().text()
        data = self.database.get_user_history(contact_login)
        data.sort(key=lambda x: x.date, reverse=True)
        logger.info('response received %s', data)
        acc_name = self.client.account_name
        for message_history in data:
            if message_history.contact_login == acc_name:
                self.__add_received_msg_to_model(message_history.date, message_history.message)
            else:
                self.__add_sent_msg_to_model(message_history.date, message_history.message)

    def __add_sent_msg_to_model(self, date_time, message):
        mess = QStandardItem(f'Sent at {date_time.replace(microsecond=0)}:\n {message}')
        mess.setEditable(False)
        mess.setTextAlignment(Qt.AlignRight)
        mess.setBackground(QBrush(QColor(228, 242, 255)))
        self.chat_model.appendRow(mess)

    def __add_received_msg_to_model(self, date_time, message):
        mess = QStandardItem(f'Received at {date_time.replace(microsecond=0)}:\n {message}')
        mess.setEditable(False)
        mess.setBackground(QBrush(QColor(230, 230, 255)))
        mess.setTextAlignment(Qt.AlignLeft)
        self.appendRow(mess)

    def add_contact_to_list(self):
        contact = self.input_contact_login.text()
        if contact:
            if not self.database.check_contact(contact):
                self.client.add_contact(contact, lambda response: self.add_contact_signal.emit(contact, response))
            else:
                self.label_3.setText('This contact is already in your contact list')

    @pyqtSlot(str, dict)
    def show_new_contact(self, contact, response):
        if response.get(ServerResponseFieldName.RESPONSE.value) == ResponseCode.OK.value:
            self.contacts_list.addItem(contact)
            self.database.add_contact(contact)
            self.database.session.commit()
        if response.get(ServerResponseFieldName.RESPONSE.value) == ResponseCode.BAD_REQUEST.value:
            self.label_3.setText('This contact is absent in messenger')

    def del_contact_from_list(self):
        contact = self.input_contact_login.text()
        if contact:
            if self.database.check_contact(contact):
                self.client.del_contact(contact, lambda response: self.del_contact_signal.emit(contact, response))
                return
            self.label_3.setText('This login is absent in your contact list')

    @pyqtSlot(str, dict)
    def remove_contact(self, contact, response):
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
