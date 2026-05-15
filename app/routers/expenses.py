from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)


@router.post("/", response_model=schemas.ExpenseOut, status_code=201)
async def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a new expense for the authenticated user."""
    return crud.create_expense(db, expense, owner_id=current_user.user_id)


@router.get("/", response_model=List[schemas.ExpenseOut])
async def get_expenses(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Retrieve all expenses for the authenticated user.
    Optionally filter by category using the `category` query parameter.
    """
    if category:
        return crud.get_expenses_by_category(db, current_user.user_id, category)
    return crud.get_expenses(db, current_user.user_id)


@router.get("/month/{year}/{month}", response_model=List[schemas.ExpenseOut])
async def get_expenses_by_month(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retrieve expenses for the authenticated user filtered by year and month."""
    return crud.get_expenses_by_month(db, current_user.user_id, year, month)


@router.get("/week/{year}/{week}", response_model=List[schemas.ExpenseOut])
async def get_expenses_by_week(
    year: int,
    week: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retrieve expenses for the authenticated user filtered by ISO week number."""
    return crud.get_expenses_by_week(db, current_user.user_id, year, week)


@router.get("/day/{year}/{month}/{day}", response_model=List[schemas.ExpenseOut])
async def get_expenses_by_day(
    year: int,
    month: int,
    day: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retrieve expenses for the authenticated user on a specific date."""
    return crud.get_expenses_by_day(db, current_user.user_id, year, month, day)
