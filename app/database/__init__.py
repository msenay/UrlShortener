import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from app.settings import settings

logger = logging.getLogger(__name__)

Base = declarative_base()
metadata = MetaData()
engine = create_engine(settings.db_url, pool_pre_ping=True)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
