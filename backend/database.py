''' The central file for our database setup. '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL_DATABASE = 'mysql+pymysql://root:adminpass1word!@mysql.bktp-gradproapp-db/VTGrads_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()