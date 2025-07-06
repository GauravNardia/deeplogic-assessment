from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats/issues-by-severity")
def issues_by_severity(db: Session = Depends(get_db)):
    severities = ["LOW", "MEDIUM", "HIGH"]
    return {
        s: db.query(models.Issue).filter_by(severity=s, status="OPEN").count()
        for s in severities
    }
