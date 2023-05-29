import os
 
from sqlalchemy import create_engine
from sqlalchemy.orm import Session



from db.models import Base, Question


def make_engine():
    return create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postge_db:5432/{os.getenv('POSTGRES_DB')}") 

    


def create_db():
    Base.metadata.create_all(make_engine())


def make_session():
    return Session(make_engine())

def get_ids():
    with make_session() as session:
        ids = session.query(Question.id).all()
        if ids:
            return [id[0] for id in ids]
        return []
