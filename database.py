from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:neyong_lim123@localhost:5432/fastAPI-explore"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
