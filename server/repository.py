from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Repository:
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'clients'
        login = Column(String, primary_key=True)
        name = Column(String)
        surname = Column(String)
        password = Column(Text)
        birthdate = Column(String)

        def __init__(self, login, name, surname, password, birthdate):
            self.login = login
            self.name = name
            self.surname = surname
            self.password = password
            self.birthdate = birthdate

        def __repr__(self):
            return f'Client {self.login} with name {self.name}'

    class UserHistory(Base):
        __tablename__ = 'clients_history'
        client_id = Column(Integer, primary_key=True)
        login = Column(String, ForeignKey('clients.login'), nullable=False)
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
        owner_login = Column(String, ForeignKey('clients.login'), nullable=False)
        contact_login = Column(String, ForeignKey('clients.login'))

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

    def add_history(self, history: UserHistory):
        self.session.add(history)
        self.session.commit()

    def load_users(self):
        return self.session.query(self.User)

    def add_user(self, user: User):
        self.session.add(user)
        self.session.commit()

    def del_user(self, login):
        self.session.query(self.User).filter_by(login=login).delete()
        self.session.commit()

    def get_user(self, login: str) -> User:
        return self.session.query(self.User).filter_by(login=login)

    def connect_to_messenger(self, client_login, ip_address):
        user_history = self.UserHistory(client_login, ip_address, datetime.now())
        self.session.add(user_history)
        self.session.commit()

    def add_contact(self, owner: str, contact_login: str):
        contact = self.Contact(owner, contact_login)
        self.session.add(contact)
        self.session.commit()

    def del_contact(self, owner: str, contact: str):
        self.session.query(self.Contact) \
            .filter_by(owner_login=owner, contact_login=contact) \
            .delete()
        self.session.commit()

    def get_contacts(self, owner: str):
        return self.session.query(self.Contact.contact_login).filter_by(owner_login=owner)


if __name__ == '__main__':
    repository = Repository('sqlite:///./clients.sqlite')
    # repository.add_user(Repository.User('madonna','madonna', 'lora', '123456', date(1958,8,16)))
    # print(list(repository.get_contacts('jlo')))  # [('madonna',), ('justin',), ('tommy',), ('rihanna',)]
