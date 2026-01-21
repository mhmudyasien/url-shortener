import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

@app.post("/shorten", response_model=schemas.URLInfo)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    """
    Shorten a URL.
    """
    # Create URL in DB
    db_url = crud.create_url(db=db, url=url)
    return schemas.URLInfo(url=db_url.original_url, short_code=db_url.short_code, original_url=db_url.original_url)

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redirect to the original URL.
    """
    # Check Database
    db_url = crud.get_url_by_short_code(db, short_code=short_code)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=db_url.original_url)
