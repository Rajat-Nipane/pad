from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>/<hostname>/<database_name>'


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>/<hostname>/<database_name>'

# to directly connect with every data exposed
# SQLALCHEMY_DATABASE_URL = ('postgresql://postgres:%s@localhost/fastapi' % quote_plus("UsePostgre@2023"))


#using environment variable
#  
host = settings.database_password
# SQLALCHEMY_DATABASE_URL = ("postgresql://{}:%s@{}:{}/{}".format(settings.database_username,settings.database_password,settings.database_hostname,settings.database_port,settings.database_name))
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = ('postgresql://postgres:%s@localhost/fastapi' % quote_plus(settings.database_password))

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




import psycopg2
from psycopg2.extras import RealDictCursor
import time
#Connect to DB directly and user cursor and pure sql query
# while(True):
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres',password='UsePostgre@2023',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(" db connected ")
#         break
#     except Exception as error:
#         print("db connecion failed")
#         print("Error : ",error)
#         time.sleep(2)