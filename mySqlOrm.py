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
    file_name = Column(String(255))
    download_date = Column(String(255))
    create_date = Column(String(255))
    main_site_url = Column(String(255))
    image_url = Column(String(1024))

    def __str__(self):
        return 'id = {}, file_name = {}, download_date = {},' \
               ' create_date = {}, main_site_url = {}, image_url = {}'.format(self.id,
                                                                              self.file_name,
                                                                              self.download_date,
                                                                              self.create_date,
                                                                              self.main_site_url,
                                                                              self.image_url)


def queryImage():
    query = session.query(Image)
    return query


def insertImage(file_name, download_date, create_date, main_site_url, image_url):
    image = Image(file_name=file_name, download_date=download_date, create_date=create_date,
                  main_site_url=main_site_url, image_url=image_url)
    session.add(image)
    session.commit()


def closeSession():
    session.close()


# call base to create table
if __name__ == '__main__':
    Base.metadata.create_all(engine)
