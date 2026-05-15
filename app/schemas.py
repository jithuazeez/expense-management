from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ExpenseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    expense_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TotalsOut(BaseModel):
    total_expenses: float
    total_salary: float
    remaining_amount: float


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    salary: float = Field(..., gt=0)


class UserOut(BaseModel):
    user_id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
