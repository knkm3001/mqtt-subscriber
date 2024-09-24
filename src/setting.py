import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_ROOT_PASSWORD')
host = os.getenv('MYSQL_HOST_NAME')
db_name = os.getenv('MYSQL_DB_NAME')

DATABASE = f'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}'

Engine = create_engine(
    DATABASE,
    echo=False,  # sql吐き出すかどうか
)


session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=Engine
    )
)

Base = declarative_base()
Base.query = session.query_property()