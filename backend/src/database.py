''' The central file for our database setup. '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL_DATABASE = 'mysql+pymysql://root:Danny2498@localhost:3306/VTGrads_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
