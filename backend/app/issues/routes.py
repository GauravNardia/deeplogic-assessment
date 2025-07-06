from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from typing import List
from jose import JWTError, jwt
import os

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = db.query(models.User).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")


@router.post("/issues")
def create_issue(
    issue: schemas.IssueCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role not in ["REPORTER", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Only reporters and admins can create issues")
    
    new_issue = models.Issue(
        title=issue.title,
        description=issue.description,
        severity=issue.severity,
        status=issue.status,
        user_id=user.id
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue


@router.get("/issues", response_model=List[schemas.IssueResponse])
def get_issues(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role == "REPORTER":
        return db.query(models.Issue).filter_by(user_id=user.id).all()
    elif user.role == "MAINTAINER":
        return db.query(models.Issue).filter_by(assigned_to=user.id).all()
    elif user.role == "ADMIN":
        return db.query(models.Issue).all()
    else:
        raise HTTPException(status_code=403, detail="Invalid role")


@router.patch("/issues/{issue_id}")
def update_issue(
    issue_id: int,
    data: schemas.IssueBase,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    issue = db.query(models.Issue).filter_by(id=issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if user.role not in ["MAINTAINER", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Not allowed to update")

    # Maintainer: Can only update status and tags
    if data.status:
        issue.status = data.status
    if hasattr(data, "tags") and data.tags:
        issue.tags = data.tags

    # Admin can do everything
    if user.role == "ADMIN":
        if data.severity:
            issue.severity = data.severity
        if data.assigned_to:
            issue.assigned_to = data.assigned_to
        if data.title:
            issue.title = data.title
        if data.description:
            issue.description = data.description

    db.commit()
    db.refresh(issue)
    return {"detail": "Issue updated"}
