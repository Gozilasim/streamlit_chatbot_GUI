
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import SQLAlchemyError


DATABASE_URL = "sqlite:///chat_history1.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    import Message
    import Session
    Base.metadata.create_all(bind=engine)

#handle database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()

    return db