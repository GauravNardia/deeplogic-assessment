from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    REPORTER = "REPORTER"
    MAINTAINER = "MAINTAINER"
    ADMIN = "ADMIN"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class IssueBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = ""
    severity: Optional[str] = "LOW"
    status: Optional[str] = "OPEN"
    assigned_to: Optional[int] = None

class IssueCreate(IssueBase):
    title: str
    description: str
    severity: str
    status: str


class IssueResponse(IssueBase):
    id: int
    user_id: int

    class Config:
       from_attributes = True

