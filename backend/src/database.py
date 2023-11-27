''' The central file for our database setup. '''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

if os.environ.get("ENVIRONMENT") != "production":
    from dotenv import load_dotenv
    load_dotenv()

host = os.environ.get("DB_HOST", "default_host")
user = os.environ.get("DB_USER", "default_user")
password = os.environ.get("DB_PASSWORD", "")
database = os.environ.get("DB_NAME", "default_database")
port = os.environ.get("DB_PORT", "3306")

URL_DATABASE = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
