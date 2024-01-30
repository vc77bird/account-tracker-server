from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sys import platform

URL_DATABASE = 'sqlite:///../database/eReg.db'

if platform == "linux" or platform == "linux2":
    URL_DATABASE = "sqlite:////code/database/eReg.db"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()