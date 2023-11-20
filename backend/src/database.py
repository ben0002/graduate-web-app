<<<<<<< HEAD
''' The central file for our database setup. '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL_DATABASE = 'mysql+pymysql://root:root@localhost:3306/VTGrads_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
=======
''' The central file for our database setup. '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


URL_DATABASE = 'mysql+pymysql://root:root@localhost:3306/VTGrads_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> d28d3b6d81e30ce70c78ee26bc5300dd23c11036
