from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.users import AuthTokenResponse, UserCreate, UserLogin
from services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, payload)


@router.post("/login", response_model=AuthTokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, payload)
