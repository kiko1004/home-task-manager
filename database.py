import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import get_config

config = get_config()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import all modules here that might define models so that
    # they will be registered properly on the metadata.
    import models
    Base.metadata.create_all(bind=engine)
