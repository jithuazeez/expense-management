from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime, timezone, timedelta


def create_expense(db: Session, expenses: schemas.ExpenseCreate):

    db_expense = models.Expense(**expenses.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expense(db: Session, user_id: int):
    return db.query(models.Expense).filter(
        models.Expense.owner_id == user_id).all()

def get_expenses_by_month(db: Session, user_id: int, year: int, month: int):
    return db.query(models.Expense).filter(
        models.Expense.owner_id == user_id,
        models.Expense.created_at.year == year,
        models.Expense.created_at.month == month).all()

def get_expenses_by_week(db: Session, user_id: int, year: int, week: int):
    return db.query(models.Expense).filter(
        models.Expense.owner_id == user_id,
        models.Expense.created_at.year == year,
        models.Expense.created_at.week == week).all()

def get_expenses_by_day(db: Session, user_id: int, year: int, month: int, day: int):
    start = datetime(year, month, day)
    end = start + timedelta(days = 1)
    return db.query(models.Expense).filter(user_id == user_id, models.Expense.created_at >= start, models.Expense.created_at < end).all()

def get_expense_by_category(db: Session, user_id: int, category: str):
    return db.query(models.Expense).filter(user_id == user_id, models.Expense.category == category).all()

def get_total_expenses(db: Session, user_id: int):
    return db.query(models.Expense).filter(user_id == user_id).sum(models.Expense.amount)

def get_total_salary(db: Session, user_id: int):
    return db.query(models.User).filter(user_id == user_id).first().salary

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user