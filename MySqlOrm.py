from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, INT
from sqlalchemy.orm import sessionmaker


#                      db type   user   pwd       db path         db name
engine = create_engine("mysql+mysqldb://root:best930901@localhost:3306/python_db")

Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    __tablename__ = 'user'

    id = Column(INT, primary_key=True)
    name = Column(String(20))

class Image(Base):
    __tablename__ = 'image'

    id = Column(INT, primary_key=True)
    file_name = Column(String(20))
    download_date = Column(String(255))
    create_date = Column(String(255))
    main_site_url = Column(String(255))

# call base to create table
Base.metadata.create_all(engine)

