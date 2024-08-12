import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import crud
from app.database.session import get_db
from app.models.url_shortener import URLCreate, URL

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/urls/", response_model=URL)
def create_url(url: URLCreate, db: Session = Depends(get_db)):
    """
    Create a short URL.

    This endpoint creates a short URL from the given original URL. If the original URL
    already exists in the database, it returns the existing short URL.

    Args:
        url (URLCreate): The original URL to be shortened.
        db (Session): The database session.

    Returns:
        URL: The created or existing URL object containing both the original and short URLs.
    """
    db_url = crud.get_url_by_original_url(db, original_url=url.original_url)
    if db_url:
        return db_url
    return crud.create_url(db_session=db, url=url)


@router.get("/{short_url}", response_model=URL)
def read_url(short_url: str, db: Session = Depends(get_db)):
    """
    Retrieve the original URL from a short URL.

    This endpoint takes a short URL and retrieves the corresponding original URL from the database.

    Args:
        short_url (str): The short URL to be resolved to its original form.
        db (Session): The database session.

    Returns:
        URL: The URL object containing both the original and short URLs.

    Raises:
        HTTPException: If the short URL is not found in the database.
    """
    logger.info(f"Fetching URL for short_url: {short_url}")
    db_url = crud.get_url_by_short_url(db_session=db, short_url=short_url)
    logger.info(f"URL: {db_url}")
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url


@router.get("/{short_url}/redirect")
def redirect_url(short_url: str, db: Session = Depends(get_db)):
    """
    Redirect to the original URL from a short URL.

    This endpoint takes a short URL and redirects the user to the corresponding original URL.

    Args:
        short_url (str): The short URL to be resolved to its original form.
        db (Session): The database session.

    Returns:
        RedirectResponse: A response that redirects the client to the original URL.

    Raises:
        HTTPException: If the short URL is not found in the database.
    """
    db_url = crud.get_url_by_short_url(db_session=db, short_url=short_url)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=db_url.original_url)
