from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import timezone
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    amount = Column(Float, nullable = False)
    category = Column(String, nullable = False, index = True)
    created_at = Column(DateTime, nullable = False, default = datetime.now(timezone.utc))
    salary = Column(Float, nullable = False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="expenses")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True, index = True)
    username = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    expenses = relationship("Expense", back_populates="user")
    created_at = Column(DateTime, nullable = False, default = datetime.now(timezone.utc))

