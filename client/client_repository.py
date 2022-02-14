from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ClientRepository:
    Base = declarative_base()

    class MyContacts(Base):
        __tablename__ = 'my_contacts'
        login = Column(String, primary_key=True)
        name = Column(String)

    class MessageHistory(Base):
        __tablename__ = 'history'
        id = Column(Integer, primary_key=True)
        contact_login = Column(String, ForeignKey('my_contacts.login'), nullable=False)
        message = Column(Text)
        time = Column(DateTime)

    def __init__(self, url):
        self.engine = create_engine(url, echo=False, pool_recycle=7200)
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_contact(self, contact):
        if not self.session.query(self.MyContacts).filter_by(login=contact).count():
            contact_row = self.MyContacts(login=contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        self.session.query(self.MyContacts).filter_by(login=contact).delete()
        self.session.commit()

    def get_contact_list(self):
        return [contact[0] for contact in self.session.query(self.MyContacts.login).all()]  #returns list of contacts instead of tuples

    def save_message(self, from_contact, message):
        message_row = self.MessageHistory(
            contact_login=from_contact,
            message=message,
            date=datetime.now()
        )
        self.session.add(message_row)
        self.session.commit()

    def get_user_history(self, user):
        query = self.session.query(self.MessageHistory).filter_by(contact_login=user)
        return query


# if __name__ == '__main__':
#     repository = ClientRepository('sqlite:///./clients_history.sqlite')
