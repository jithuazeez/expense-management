from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user


router = APIRouter(
    prefix="/totals",
    tags=["totals"],
)


@router.get("/", response_model=schemas.TotalsOut)
async def get_totals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return total expenses, total salary, and remaining amount
    for the authenticated user.
    """
    total_expenses = crud.get_total_expenses(db, current_user.user_id)
    total_salary = crud.get_total_salary(db, current_user.user_id)
    remaining_amount = total_salary - total_expenses
    return {
        "total_expenses": total_expenses,
        "total_salary": total_salary,
        "remaining_amount": remaining_amount,
    }
