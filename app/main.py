import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db, redis_client

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/shorten", response_model=schemas.URLInfo)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    """
    Shorten a URL.
    """
    # Create URL in DB
    db_url = crud.create_url(db=db, url=url)
    
    # Cache it in Redis immediately (optional, but good for read-after-write consistency if needed)
    try:
        redis_client.set(db_url.short_code, db_url.original_url)
    except Exception as e:
        logger.error(f"Redis error: {e}")

    return schemas.URLInfo(url=db_url.original_url, short_code=db_url.short_code, original_url=db_url.original_url)

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redirect to the original URL.
    """
    # 1. Check Redis
    try:
        cached_url = redis_client.get(short_code)
        if cached_url:
            logger.info(f"Cache hit for {short_code}")
            return RedirectResponse(url=cached_url)
    except Exception as e:
        logger.error(f"Redis error: {e}")

    # 2. Check Database
    db_url = crud.get_url_by_short_code(db, short_code=short_code)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    # 3. Update Redis if found in DB
    try:
        redis_client.set(short_code, db_url.original_url)
    except Exception as e:
        logger.error(f"Redis error: {e}")

    return RedirectResponse(url=db_url.original_url)
