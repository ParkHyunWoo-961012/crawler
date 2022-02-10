from sqlalchemy import create_engine, Column, String, DateTime, UnicodeText, text
from sqlalchemy.ext.declarative import declarative_base
import datetime


DeclarativeBase = declarative_base()


def db_connect():
    return create_engine("mysql+pymysql://root:password@localhost/news_db")


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine, checkfirst=True)



class Content(DeclarativeBase):
    __tablename__ = 'allnews'

    id = Column('id', String(50), primary_key=True)
    category = Column('category', String(50), nullable=False, server_default='')
    title = Column('title', String(1000), nullable=False, server_default='')
    content = Column('content', UnicodeText, nullable=False)
    created_dt = Column('created_dt', DateTime, nullable=False, server_default=str(datetime.datetime.min))
    updated_dt = Column('updated_dt', DateTime, nullable=False, server_default=str(datetime.datetime.min))

    def __init__(self):
        self.id = ''
        self.category = ''
        self.title = ''
        self.content = ''
        self.created_dt = datetime.datetime.min
        self.updated_dt = datetime.datetime.min

