import random
import string
from sqlalchemy.orm import Session
from . import models, schemas

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_url(db: Session, url: schemas.URLCreate):
    code = generate_short_code()
    # Ensure uniqueness (simple retry logic could be added here, but for simplicity we assume low collision probability for now or unique constraint handling)
    # A robust solution would check if code exists.
    
    # Check if code exists to be safe
    while get_url_by_short_code(db, code):
        code = generate_short_code()

    db_url = models.URL(original_url=str(url.url), short_code=code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_short_code(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()
