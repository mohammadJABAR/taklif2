from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "mysql+pymysql://resume_user:password123@localhost/resume_db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()