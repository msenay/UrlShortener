import logging
import random
import string
from sqlalchemy.orm import Session

from app.cache.url_shortener import cache_result
from app.database import Base, engine
from app.database.models import URL
from app.models.url_shortener import URLCreate

logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize the database.

    This function creates all tables in the database that are defined in the SQLAlchemy
    models. It should be called once when setting up the application for the first time.
    """
    Base.metadata.create_all(bind=engine)


@cache_result(key_prefix="url_by_short_url", expiration_seconds=30)
def get_url_by_short_url(db_session: Session, short_url: str):
    """
    Retrieve a URL by its short version.

    This function queries the database for a URL object that matches the provided short URL.
    The result is cached for future requests.

    Args:
        db_session (Session): The database session.
        short_url (str): The short URL to be looked up.

    Returns:
        URL: The URL object if found, otherwise None.
    """
    logger.info(f"Fetching URL for short_url: {short_url}")
    return db_session.query(URL).filter(URL.short_url == short_url).first()


@cache_result(key_prefix="url_by_original_url", expiration_seconds=30)
def get_url_by_original_url(db_session: Session, original_url: str):
    """
    Retrieve a URL by its original version.

    This function queries the database for a URL object that matches the provided original URL.
    The result is cached for future requests.

    Args:
        db_session (Session): The database session.
        original_url (str): The original URL to be looked up.

    Returns:
        URL: The URL object if found, otherwise None.
    """
    logger.info(f"Fetching URL for original_url: {original_url}")
    return db_session.query(URL).filter(URL.original_url == original_url).first()


def create_url(db_session: Session, url: URLCreate):
    """
    Create a new short URL.

    This function generates a new short URL, saves it to the database, and returns the
    created URL object.

    Args:
        db_session (Session): The database session.
        url (URLCreate): The URL data containing the original URL.

    Returns:
        URL: The created URL object with both the original and short URLs.
    """
    short_url = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    db_url = URL(original_url=url.original_url, short_url=short_url)
    db_session.add(db_url)
    db_session.commit()
    db_session.refresh(db_url)
    return db_url
