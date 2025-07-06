from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
import time
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

max_retries = 10
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"Waiting for database... attempt {i + 1}/{max_retries}")
        time.sleep(3)
else:
    raise Exception("Could not connect to the database after several attempts.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
