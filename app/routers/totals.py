from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db


router = APIRouter(
    prefix = "/totals",
    tags = ["totals"]
)

@router.get("/", response_model = schemas.TotalsOut)
async def get_totals(db: Session = Depends(get_db)):
    total_expenses = crud.get_total_expenses(db)
    total_salary = crud.get_total_salary(db)
    remaining_amount = total_salary - total_expenses
    return {"total_expenses": total_expenses, "total_salary": total_salary, "remaining_amount": remaining_amount}
