from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Define Role Enum
class RoleEnum(str, enum.Enum):
    REPORTER = "REPORTER"
    MAINTAINER = "MAINTAINER"
    ADMIN = "ADMIN"

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # You were missing this!
    role = Column(SqlEnum(RoleEnum), nullable=False)

    reported_issues = relationship(
        "Issue", back_populates="reporter", foreign_keys="Issue.user_id"
    )
    assigned_issues = relationship(
        "Issue", back_populates="assignee", foreign_keys="Issue.assigned_to"
    )

# Issue Model
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="OPEN")
    severity = Column(String, default="LOW")

    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    reporter = relationship(
        "User", back_populates="reported_issues", foreign_keys=[user_id]
    )
    assignee = relationship(
        "User", back_populates="assigned_issues", foreign_keys=[assigned_to]
    )
