from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db



router = APIRouter(
    prefix = "/expenses",
    tags = ["expenses"]
)

@router.post("/", response_model = schemas.ExpenseOut,status_code = 201)
async def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)

@router.get("/", response_model = List[schemas.ExpenseOut])
def get_expenses(category: Optional[str] = None, db: Session = Depends(get_db)):
    if category:
        return crud.get_expense_by_category(db, category)
    else:
        return crud.get_expenses(db)

@router.get("/month/{year}/{month}", response_model = List[schemas.ExpenseOut])
def get_expenses_month(year:int, month:int, db: Session = Depends(get_db)):
    return crud.get_expenses_by_month(db, year, month)

@router.get("/week/{year}/{week}", response_model = List[schemas.ExpenseOut])
def get_expenses_week(year:int, week:int, db: Session = Depends(get_db)):
    return crud.get_expenses_by_week(db, year, week)

@router.get("/day/{year}/{month}/{day}", response_model = List[schemas.ExpenseOut])
def get_expenses_day(year:int, month:int, day:int, db: Session = Depends(get_db)):
    return crud.get_expenses_by_day(db, year, month, day)

@router.get("/total", response_model = schemas.TotalsOut)
def get_total_expenses(db: Session = Depends(get_db)):
    return crud.get_total_expenses(db)

@router.get("/salary", response_model = schemas.SalaryOut)
def get_total_salary(db: Session = Depends(get_db)):
    return crud.get_total_salary(db)

  