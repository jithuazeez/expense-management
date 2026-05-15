from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user, hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.post("/register", response_model = schemas.UserOut, status_code = 201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user, hashed_password = hash_password(user.password))

@router.post("/token", response_model = schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    access_token = create_access_token(data = {"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}