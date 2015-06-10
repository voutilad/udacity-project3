import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine

#TODO: Document these classes

__DATABASE_NAME = 'catalog'

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship(Category)
    #TODO: use backref capability for cascading deletes?

engine = create_engine('postgresql://vagrant@/' + __DATABASE_NAME)

try:
    Base.metadata.create_all(engine)

except OperationalError:
    print 'Database does not exist. Attempting to first create database ' + __DATABASE_NAME

    try:
        #See: http://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy
        conn = create_engine('postgresql://vagrant@/postgres').connect()
        conn.execute('commit')
        conn.execute('CREATE DATABASE ' + __DATABASE_NAME + ';')
        conn.close()

        Base.metadata.create_all(engine)

    except Exception as e:
        print 'Still failed. :-('
        print e
