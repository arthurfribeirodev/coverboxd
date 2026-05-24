from models import db
from sqlalchemy.orm import sessionmaker

def session_grab():

    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()