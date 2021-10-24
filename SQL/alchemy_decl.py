from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///data.db')

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True),
    user_tg_id = Column(Integer, ForeignKey('Event.event_user_owner_id'))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    Event = relationship('Event')


class Event(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    photo = Column(String, nullable=False)
    description = Column(String, nullable=False)
    data_finish = Column(String, nullable=False)
    Users = relationship('Users')


Base.metadata.create_all(engine)
