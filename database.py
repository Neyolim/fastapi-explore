from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:neyong_lim@localhost:5432/telusko"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
