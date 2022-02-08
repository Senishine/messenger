import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QTableWidget, QPushButton, \
    QLineEdit, QFileDialog
from PyQt5.uic import loadUi

from server.repository import Repository
from server.utils import get_config, get_config_path


class Admin(QMainWindow):
    def __init__(self, config=None):
        super(Admin, self).__init__()
        loadUi('admin.ui', self)
        self.config = config if config else get_config()
        self.repository = Repository(self.config['SETTINGS']['database_url'])
        self.info.currentChanged.connect(self.tab_changed)
        self.users_table = self.info.widget(0).findChild(QTableWidget)
        self.stats_table = self.info.widget(1).findChild(QTableWidget)

        # settings form
        settings_widget = self.info.widget(2)
        self.db_url_line = settings_widget.findChild(QLineEdit, 'db_url')
        self.port_line = settings_widget.findChild(QLineEdit, 'port')

        reg_ex = QRegExp("[0-9]{1,5}")
        self.port_line.setValidator(QRegExpValidator(reg_ex, self.port_line))

        self.listen_address_line = settings_widget.findChild(QLineEdit, 'listen_address')
        self.save_settings_btn = settings_widget.findChild(QPushButton, 'save_btn')
        self.save_settings_btn.clicked.connect(self.save_server_settings)
        # ~ settings form

        self.select_btn = settings_widget.findChild(QPushButton, 'select_btn')
        self.select_btn.clicked.connect(self.show_file_dialog)

        self.exit_btn.clicked.connect(sys.exit)
        self.load_users()

    def show_file_dialog(self):
        url: str = self.db_url_line.text()
        if url.startswith('sqlite:///'):
            url = url[len('sqlite:///'):]
        else:
            url = ''
        path = QFileDialog.getOpenFileName(self, 'Open a database file', url,
                                           'All Files (*.*)')
        if path == ('', ''):
            return
        self.db_url_line.setText(f'sqlite:///{path[0]}')

    def tab_changed(self, index):
        if index == 0:
            self.load_users()
        elif index == 1:
            self.load_stats()
        elif index == 2:
            self.load_server_settings()
        else:
            raise ValueError(f'Unexpected tab index selected [index={index}]')

    def load_users(self):
        self.users_table.setRowCount(0)
        current_row = 0
        for user in self.repository.load_users():
            self.users_table.setRowCount(current_row + 1)
            self.users_table.setItem(current_row, 0, Admin.create_read_only_cell(user.login))
            self.users_table.setItem(current_row, 1, Admin.create_read_only_cell(user.name))
            self.users_table.setItem(current_row, 2, Admin.create_read_only_cell(user.surname))
            self.users_table.setItem(current_row, 3, Admin.create_read_only_cell("unknown"))
            del_btn = QPushButton(self.users_table)
            del_btn.setText('X')
            del_btn.clicked.connect(lambda: self.del_user(user.login))
            self.users_table.setCellWidget(current_row, 4, del_btn)
            current_row += 1

    def del_user(self, login):
        self.repository.del_user(login)
        self.load_users()

    def load_stats(self):
        self.stats_table.setRowCount(0)
        current_row = 0
        for history in self.repository.get_all_user_history():
            self.stats_table.setRowCount(current_row + 1)
            self.stats_table.setItem(current_row, 0, Admin.create_read_only_cell(history.login))
            self.stats_table.setItem(current_row, 1, Admin.create_read_only_cell(str(history.login_time)))
            self.stats_table.setItem(current_row, 2, Admin.create_read_only_cell(history.ip_address))
            current_row += 1

    @staticmethod
    def create_read_only_cell(text):
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable ^ QtCore.Qt.ItemIsSelectable)
        return item

    def load_server_settings(self):
        config = get_config()
        settings = config['SETTINGS']
        self.db_url_line.setText(settings['database_url'])
        self.port_line.setText(settings['port'])
        self.listen_address_line.setText(settings['listen_address'])

    def save_server_settings(self):
        message = QMessageBox()
        self.config['SETTINGS']['database_url'] = self.db_url_line.text()
        try:
            port = int(self.port_line.text())
        except ValueError:
            message.warning(self.info, 'Error', 'Port value must be an integer value')
        else:
            self.config['SETTINGS']['listen_address'] = self.listen_address_line.text()
            if 1023 < port < 65536:
                self.config['SETTINGS']['port'] = str(port)
                with open(get_config_path(), 'w') as conf:
                    self.config.write(conf)
                    message.information(
                        self.info, 'OK', 'Settings were saved, will be applied on the next server start'
                    )
            else:
                message.warning(
                    self.info,
                    'Error',
                    'Port must be in range from 1024 to 65536'
                )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_page = Admin()
    admin_page.show()
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')
