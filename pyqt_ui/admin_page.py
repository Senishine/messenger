import sys, sqlite3

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow, QTabWidget, QFileDialog, qApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Admin(QMainWindow):
    def __init__(self):
        super(Admin, self).__init__()
        loadUi('admin.ui', self)
        self.loaddata('sqlite:///../clients.sqlite')

    def loaddata(self, database):
        self.engine = create_engine(database, echo=False, pool_recycle=7200)
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        query =  self.session.query(self.User)
        for row in query:



        # self.exit_btn.clicked.connect(qApp.quit)

    class UsersListModel(QTabWidget):
        # Класс модели списка пользователей
        def __init__(self, database=None):
            super().__init__()
            self.database = database

        def fill_users_model(self, data):
            for row in data:
                login, name, surname, birthdate = row
                user_login = QStandardItem(login)
                user_login.setEditable(False)
                user_name = QStandardItem(name)
                user_name.setEditable(False)
                user_surname = QStandardItem(str(surname))
                user_surname.setEditable(False)
                birthdate.setEditable(False)
                self.appendRow([login, name, surname, birthdate])
            if self.database:
                data = self.database.users_active()
                self.fill_model(data)

    class StatisticInfoModel(QTabWidget):

        def __init__(self, database=None):
            super().__init__()
            self.database = database

        def fill_model(self, data):
            for row in data:
                login, last_login_time, server_settings = row
                login = QStandardItem(login)
                login.setEditable(False)
                last_login_time = QStandardItem(last_login_time)
                last_login_time.setEditable(False)
                server_settings = QStandardItem(server_settings)
                server_settings.setEditable(False)
                self.appendRow([login, last_login_time, server_settings])

        def fill_from_db(self):
            if self.database:
                data = self.database.message_history()
                self.fill_model(data)

    class ServerSettings(QTabWidget):
        def __init__(self, dialog, database=None):
            super().__init__()
            self.database = database
            self.dialog = dialog
            self.select_btn.clicked.connect(self.open_file_dialog)
            self.save_btn.clicked.connect(self.save)

        def open_file_dialog(self):
            self.dialog = QFileDialog(self)
            path = self.dialog.getExistingDirectory()
            self.path_to_file.insert(path)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_page = Admin()
    admin_page.show()
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')

