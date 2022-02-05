from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Repository:
    Base = declarative_base()

    class Client(Base):
        __tablename__ = 'clients'
        login = Column(String, primary_key=True)
        name = Column(String)
        surname = Column(String)
        password = Column(Text)

        def __init__(self, login, name, surname, password):
            self.login = login
            self.name = name
            self.surname = surname
            self.password = password

        def __repr__(self):
            return f'Client {self.login} with name {self.name}'

    class ClientsHistory(Base):
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
        client_login = Column(String, ForeignKey('clients.login'))

        def __init__(self, owner_login, client_login):
            self.owner_login = owner_login
            self.client_login = client_login

        def __repr__(self):
            return f'Owner {self.owner_login}, contacts: [{self.client_login}]'

    def __init__(self, url):
        self.engine = create_engine(url, echo=False, pool_recycle=7200)
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, user: Client):
        self.session.add(user)
        self.session.commit()

    def get_user(self, login: str) -> Client:
        return self.session.query(self.Client).filter_by(login=login)

    def connect_to_messenger(self, client_login, ip_address):
        user_history = self.ClientsHistory(client_login, ip_address, datetime.now())
        self.session.add(user_history)
        self.session.commit()

    def add_contact(self, owner: str, contact_login: str):
        contact = self.Contact(owner, contact_login)
        self.session.add(contact)
        self.session.commit()

    def del_contact(self, owner: str, contact_login: str):
        self.session.query(self.Contact) \
            .filter_by(owner_login=owner, client_login=contact_login) \
            .delete()
        self.session.commit()

    def get_contacts(self, owner: str):
        return self.session.query(self.Contact).filter_by(owner_login=owner)


if __name__ == '__main__':
    repository = Repository('sqlite:///./clients.sqlite')
    # repository.add_user(Repository.Client('madonna','madonna', 'lora', '123456'))
    # repository.add_user(Repository.Client('jlo','jennifer', 'lo','963852'))
    # repository.add_user(Repository.Client('justin','justin', 'timberlake','justin111'))
    # repository.add_user(Repository.Client('tommy','tom', 'kruz','terminator'))

    repository.add_contact('jlo', 'madonna')
    repository.add_contact('tommy', 'justin')

    for c in repository.get_contacts('jlo'):
        print(c)


