import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget

from client.client import Client


class WelcomeForm(QDialog):
    def __init__(self):
        super(WelcomeForm, self).__init__()
        loadUi('welcome_form.ui', self)
        self.loginbtn.clicked.connect(self.go_to_login)
        self.sign_up_btn.clicked.connect(self.sign_up_for_messenger)

    def go_to_login(self):
        login_obj = LoginForm()
        widget.addWidget(login_obj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_for_messenger(self):
        registration = SignUpForm()
        widget.addWidget(registration)
        widget.setCurrentIndex(widget.currentIndex()+1)


class LoginForm(QDialog):
    def __init__(self):
        super(LoginForm, self).__init__()
        loadUi('login.ui', self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbtn.clicked.connect(self.connect_to_chat)
        self.back_btn.clicked.connect(self.back_to_welcome)

    def connect_to_chat(self):
        client_login = self.login_field.text()
        password = self.password_field.text()

        if len(client_login) == 0 or len(password) == 0:
            self.error_field.setText('Please input all fields')
        else:
            client = Client(client_login, lambda x: x)
            client.connect()

    def back_to_welcome(self):
        welcome_form = WelcomeForm()
        widget.addWidget(welcome_form)
        widget.setCurrentIndex(widget.currentIndex()+1)


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

        if len(user_login)==0 or len(password)==0 or len(confirm_password)==0 or len(name)==0 or len(surname)==0:
            self.error_field.setText('Please fill in all inputs')
        elif password != confirm_password:
            self.error_field.setText('Password don\'t match, please try again')
        else:
            account = AccountForm()
            widget.addWidget(account)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def back_to_welcome(self):
        welcome_form = WelcomeForm()
        widget.addWidget(welcome_form)
        widget.setCurrentIndex(widget.currentIndex()+1)


class AccountForm(QDialog):
    def __init__(self):
        super(AccountForm, self).__init__()
        loadUi('account_form.ui', self)









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

