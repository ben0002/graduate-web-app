''' The central file for our database setup. '''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

if os.environ.get("ENVIRONMENT") != "production":
    from dotenv import load_dotenv
    load_dotenv()

host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_NAME")

URL_DATABASE = f"mysql+pymysql://{user}:{password}@{host}/{database}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)