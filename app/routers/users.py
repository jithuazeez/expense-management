from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user, hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=schemas.UserOut, status_code=201)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user. Provide a username, password, and monthly salary."""
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return crud.create_user(db, user, hashed_password=hash_password(user.password))


@router.post("/token", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Obtain a JWT access token by providing valid credentials."""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
