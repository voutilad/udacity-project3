''' Database binding and initialization using SQLAlchemy '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

__DATABASE_NAME = 'catalog'
__DATABAUSE_URI = 'postgresql://vagrant@/' + __DATABASE_NAME
ENGINE = create_engine(__DATABAUSE_URI)
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=ENGINE))
BASE = declarative_base()
BASE.query = DB_SESSION.query_property()

def init_db():
    ''' Initialize and bootstrap the database for the Catalog application '''
    from models import Item, Category

    try:
        BASE.metadata.create_all(create_engine(__DATABAUSE_URI, echo=True))
        return True

    except OperationalError:
        print 'Database does not exist. Attempting to first create database ' + __DATABASE_NAME

        try:
            #See: http://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy
            conn = create_engine('postgresql://vagrant@/vagrant').connect()
            conn.execute('commit')
            conn.execute('CREATE DATABASE ' + __DATABASE_NAME + ';')
            conn.close()

            BASE.metadata.create_all(create_engine(__DATABAUSE_URI, echo=True))
            return True

        except Exception as error:
            print 'Still failed:'
            print error

        return False


if __name__ == '__main__':
    print 'Initializing dataBASE...'
    import database
    database.init_db()
