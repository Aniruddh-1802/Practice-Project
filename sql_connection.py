import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_tables import Base

engine = create_engine('mysql+pymysql://root:root@localhost:3306/project1')

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()