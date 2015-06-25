from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

__DATABASE_NAME = 'catalog'
__DATABAUSE_URI = 'postgresql://vagrant@/' + __DATABASE_NAME
engine = create_engine(__DATABAUSE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db(drop=False):
    from models import Item, Category

    try:
        Base.metadata.create_all(create_engine(__DATABAUSE_URI, echo=True))
        return True

    except OperationalError:
        print 'Database does not exist. Attempting to first create database ' + __DATABASE_NAME

        try:
            #See: http://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy
            conn = create_engine('postgresql://vagrant@/vagrant').connect()
            conn.execute('commit')
            conn.execute('CREATE DATABASE ' + __DATABASE_NAME + ';')
            conn.close()

            Base.metadata.create_all(create_engine(__DATABAUSE_URI, echo=True))
            return True

        except Exception as e:
            print 'Still failed:'
            print e

        return False


if __name__ == '__main__':
    print 'Initializing database...'
    import database
    database.init_db()
