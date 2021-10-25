from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select, and_
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.db', echo=True)

Base = declarative_base()

session = sessionmaker(bind=engine)
s = session()


class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    user_tg_id = Column(Integer, ForeignKey('Events.event_user_owner_id'))
    first_name = Column(String)
    last_name = Column(String)


class Events(Base):
    __tablename__ = 'Events'

    event_id = Column(Integer, primary_key=True)
    event_user_owner_id = Column(Integer)
    name = Column(String)
    title = Column(String)
    photo = Column(String)
    description = Column(String)
    data_finish = Column(String)


Base.metadata.create_all(engine)


def add_user_info(user_info):
    try:
        user_info_request = s.query(Users.first_name).filter(Users.user_tg_id == user_info['user_tg_id'])
        print(user_info_request[0])
        print(user_info_request)
    except:
        user_info = Users(user_tg_id=user_info['user_tg_id'],
                          first_name=user_info['first_name'],
                          last_name=user_info['last_name'])
        s.add(user_info)
        s.commit()


def add_event(event_info):
    event_info = Events(event_user_owner_id=event_info['event_user_owner_id'],
                        name=event_info['name'],
                        title=event_info['title'],
                        photo=event_info['photo'],
                        description=event_info['description'],
                        data_finish=event_info['data_finish'])
    s.add(event_info)
    s.commit()


def catalog():
    events = {}
    for row in s.query(Events):
        events[row.name] = {'title': row.title,
                            'photo': row.photo,
                            'description': row.description}
    return events