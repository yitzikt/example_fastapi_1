from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . config import settings
import time
import psycopg2


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}"\
        f":{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:isaact@localhost/fastapi_1"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect('host=localhost dbname=fastapi_1 user=postgres password=isaact')
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         break
#     except Exception as e:
#         print('Failed to connect to database')
#         print("error message: ", e)
#         time.sleep(3)