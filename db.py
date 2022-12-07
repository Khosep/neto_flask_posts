import os
import atexit
from sqlalchemy import create_engine, Column, Text, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}'
print(DSN)
engine = create_engine(DSN)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'user_table'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f'<User: {self.id}. {self.username}>'


class Post(Base):
    __tablename__ = 'post_table'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)

    user = relationship('User', backref='posts')

    def __repr__(self):
        return f'<Post: {self.id}. {self.title}>'


def create_tables():
    Base.metadata.drop_all()
    Base.metadata.create_all()


create_tables()

Session = sessionmaker(bind=engine)

# close db
atexit.register(lambda: engine.dispose())
