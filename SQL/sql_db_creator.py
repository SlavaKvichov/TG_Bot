from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

meta = MetaData()

user_id = Table('Users', meta,
                Column('user_id', Integer, primary_key=True),
                Column('user_nickname', String, nullable=False),
                Column('user_first_name', String, nullable=False)
                )
events = Table('Events', meta,
               Column('media', String, nullable=False),
               Column('event_title', String, nullable=False),
               Column('event_description', String, nullable=False)
               )
engine = create_engine('sqlite:///data.db')
meta.create_all(engine)