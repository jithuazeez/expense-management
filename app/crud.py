from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app import models, schemas
from datetime import datetime, timezone, timedelta


def create_expense(db: Session, expense: schemas.ExpenseCreate, owner_id: int):
    """Create a new expense for the given user."""
    db_expense = models.Expense(**expense.model_dump(), owner_id=owner_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, owner_id: int):
    """Return all expenses belonging to the given user."""
    return db.query(models.Expense).filter(
        models.Expense.owner_id == owner_id
    ).all()


def get_expenses_by_month(db: Session, owner_id: int, year: int, month: int):
    """Return expenses for the given user filtered by year and month."""
    return db.query(models.Expense).filter(
        models.Expense.owner_id == owner_id,
        extract("year", models.Expense.created_at) == year,
        extract("month", models.Expense.created_at) == month,
    ).all()


def get_expenses_by_week(db: Session, owner_id: int, year: int, week: int):
    """Return expenses for the given user filtered by ISO week number."""
    return db.query(models.Expense).filter(
        models.Expense.owner_id == owner_id,
        extract("year", models.Expense.created_at) == year,
        extract("week", models.Expense.created_at) == week,
    ).all()


def get_expenses_by_day(db: Session, owner_id: int, year: int, month: int, day: int):
    """Return expenses for the given user on a specific calendar day."""
    start = datetime(year, month, day, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    return db.query(models.Expense).filter(
        models.Expense.owner_id == owner_id,
        models.Expense.created_at >= start,
        models.Expense.created_at < end,
    ).all()


def get_expenses_by_category(db: Session, owner_id: int, category: str):
    """Return expenses for the given user filtered by category."""
    return db.query(models.Expense).filter(
        models.Expense.owner_id == owner_id,
        models.Expense.category == category,
    ).all()


def get_total_expenses(db: Session, owner_id: int) -> float:
    """Return the sum of all expense amounts for the given user."""
    result = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.owner_id == owner_id
    ).scalar()
    return result or 0.0


def get_total_salary(db: Session, owner_id: int) -> float:
    """Return the salary for the given user."""
    user = db.query(models.User).filter(
        models.User.user_id == owner_id
    ).first()
    return user.salary if user else 0.0


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """Create a new user with a pre-hashed password."""
    db_user = models.User(
        username=user.username,
        password=hashed_password,
        salary=user.salary,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
