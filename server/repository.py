import sqlite3
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, event, LargeBinary
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # play well with other DB backends
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class Repository:
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'clients'
        login = Column(String, primary_key=True)
        name = Column(String)
        surname = Column(String)
        password_hash = Column(LargeBinary)
        salt = Column(LargeBinary)
        birthdate = Column(String)

        def __init__(self, login, name, surname, password, salt, birthdate):
            self.login = login
            self.name = name
            self.surname = surname
            self.password_hash = password
            self.salt = salt
            self.birthdate = birthdate

        def __repr__(self):
            return f'Client {self.login} with name {self.name}'

    class UserHistory(Base):
        __tablename__ = 'clients_history'
        client_id = Column(Integer, primary_key=True)
        login = Column(String, ForeignKey('clients.login', ondelete='CASCADE'), nullable=False)
        login_time = Column(DateTime)
        ip_address = Column(String)

        def __init__(self, login, login_time, ip_address):
            self.login = login
            self.login_time = login_time
            self.ip_address = ip_address

        def __repr__(self):
            return f'Client {self.login}, time {self.login_time}'

    class Contact(Base):
        __tablename__ = 'contacts'
        contact_id = Column(Integer, primary_key=True)
        owner_login = Column(String, ForeignKey('clients.login', ondelete='CASCADE'), nullable=False)
        contact_login = Column(String, ForeignKey('clients.login', ondelete='CASCADE'))

        def __init__(self, owner_login, client_login):
            self.owner_login = owner_login
            self.contact_login = client_login

        def __str__(self):
            return self.contact_login

        # def __repr__(self):
        #     return f'Owner {self.owner_login}, contacts: [{self.contact_login}]'

    def __init__(self, url):
        self.engine = create_engine(url, echo=False, pool_recycle=7200)
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_all_user_history(self):
        return self.session.query(self.UserHistory)

    def get_user_history(self, login):
        return self.session.query(self.UserHistory).filter_by(login=login)

    def __exec(self, callback):
        try:
            callback()
            self.session.commit()
        except DatabaseError as e:
            self.session.rollback()
            raise e

    def add_history(self, history: UserHistory):
        self.__exec(lambda: self.session.add(history))

    def load_users(self):
        return self.session.query(self.User).all()

    def add_user(self, user: User):
        self.__exec(lambda: self.session.add(user))

    def del_user(self, login):
        self.__exec(lambda: self.session.query(self.User).filter_by(login=login).delete())

    def get_user(self, login: str) -> User:
        return self.session.query(self.User).filter_by(login=login).first()

    def connect_to_messenger(self, client_login, ip_address):
        user_history = self.UserHistory(client_login, ip_address, datetime.now())
        self.__exec(lambda: self.session.add(user_history))

    def add_contact(self, owner: str, contact_login: str):
        contact = self.Contact(owner, contact_login)
        self.__exec(lambda: self.session.add(contact))

    def del_contact(self, owner: str, contact: str):
        self.__exec(lambda: self.session.query(self.Contact)
                    .filter_by(owner_login=owner, contact_login=contact)
                    .delete())

    def get_contacts(self, owner: str):
        return self.session.query(self.Contact.contact_login).filter_by(owner_login=owner)

    def get_hash(self, login):
        user = self.session.query(self.User).filter_by(login=login).first()
        return user.password_hash

    def sign_up(self, login, name, surname, pass_hash, salt, birthdate):
        user_row = self.User(login=login, name=name, surname=surname, password=pass_hash, salt=salt,
                             birthdate=birthdate)
        self.__exec(lambda: self.session.add(user_row))


if __name__ == '__main__':
    repository = Repository('sqlite:///./clients.sqlite')
    # repository.add_user(Repository.User('rihanna','rihanna', 'fendi', '55555', date(1988,2,20)))
    # repository.add_user(Repository.User('jlo','jennifer', 'lo','963852', date(1958,8,16)))
    # repository.add_user(Repository.User('justin','justin', 'timberlake','justin111', date(1978,8,16)))
    # repository.add_user(Repository.User('tommy','tom', 'kruz','terminator', date(1960,8,16)))
    #
    # repository.add_contact('jlo', 'rihanna')
    # repository.add_contact('jlo', 'justin')
    # repository.add_contact('jlo', 'tommy')

    # repository.add_contact('dfhdfgjh', 'qwerty')

    # print(list(repository.get_contacts('jlo')))  # [('madonna',), ('justin',), ('tommy',), ('rihanna',)]
