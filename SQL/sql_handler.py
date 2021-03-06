from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///../Client_Bot/data.db', echo=True)

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
        user_info_request = s.query(Users).filter(Users.user_tg_id == user_info['user_tg_id'])
        print(user_info_request[0])
        user_info_request.update({'first_name': user_info['first_name'], 'last_name': user_info['last_name']})
        s.commit()
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
        events[row.event_id] = {'event_id': row.event_id,
                                'title': row.title,
                                'photo': row.photo,
                                'description': row.description,
                                'event_user_owner_id': row.event_user_owner_id}
    return events


def delete_event(event_id):
    event = s.query(Events).filter(Events.event_id == event_id)
    event.delete()
    s.commit()


def get_event_info(event_id):
    event_info = {}
    for event in s.query(Events).filter(Events.event_id == event_id):
        event_info['event_info'] = {'event_id': event.event_id,
                                    'event_user_owner_id': event.event_user_owner_id,
                                    'name': event.name,
                                    'photo': event.photo,
                                    'title': event.title,
                                    'description': event.description}
    return event_info


def get_user_info(user_tg_id):
    user_info = {}
    for user in s.query(Users).filter(Users.user_tg_id == user_tg_id):
        user_info['user_info'] = {'user_id': user.user_id,
                                  'user_tg_id': user.user_tg_id,
                                  'first_name': user.first_name,
                                  'last_name': user.last_name}
    return user_info
