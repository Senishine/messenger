"""
Модуль класса базы данных клиента
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ClientRepository:
    """
    Класс базы данных клиента
    """

    Base = declarative_base()

    class MyContacts(Base):
        """
        Класс таблицы контактов пользователя
        """
        __tablename__ = 'my_contacts'
        login = Column(String, primary_key=True)
        name = Column(String)

    class MessageHistory(Base):
        """
        Класс таблицы истории сообщений
        """
        __tablename__ = 'history'
        id = Column(Integer, primary_key=True)
        to_acc = Column(String, ForeignKey('my_contacts.login'), nullable=False)
        from_acc = Column(String, ForeignKey('my_contacts.login'), nullable=False)
        message = Column(Text)
        date = Column(DateTime)

    def __init__(self, url):
        """
        Метод инициализации. Создаётся объект движка базы данных, таблицы в базе данных
        на базе описанных классов таблиц, объект сессии
        """
        self.engine = create_engine(url, echo=False, pool_recycle=7200)
        self.Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_contact(self, contact):
        """
        Метод добавления контакта
        """
        if not self.session.query(self.MyContacts).filter_by(login=contact).count():
            contact_row = self.MyContacts(login=contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        """
        Метод удаления контакта
        """
        self.session.query(self.MyContacts).filter_by(login=contact).delete()
        self.session.commit()

    def get_contact_list(self):
        """
        Метод получения списка контактов пользователя
        """
        return [contact[0] for contact in
                self.session.query(self.MyContacts.login).all()]  # returns list of contacts instead of tuples

    def save_message(self, from_acc, to_acc, message, date=datetime.now()):
        """
        Метод сохранения сообщения в историю сообщений
        """
        message_row = self.MessageHistory(
            from_acc=from_acc,
            to_acc=to_acc,
            message=message,
            date=date
        )
        self.session.add(message_row)
        self.session.commit()

    def get_message_history(self):
        """
        Метод получения всех сообщений
        """
        return self.session.query(self.MessageHistory).all()

    def check_contact(self, contact):
        """
        Метод проверки существования контакта в таблице контактов
        """
        if self.session.query(self.MyContacts).filter_by(login=contact).count():
            return True
        return False


if __name__ == '__main__':
    repository = ClientRepository('sqlite:///db-jlo.sqlite')
    # repository.add_contact('rihanna')
    repository.add_contact('madonna')
    repository.save_message('madonna', 'rihanna', 'hi, jenny')
    data = repository.session.query(repository.MessageHistory)
    print(data)
