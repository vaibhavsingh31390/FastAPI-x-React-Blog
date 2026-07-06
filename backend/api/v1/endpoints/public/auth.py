from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.main_db import get_db
from config.main_settings import SETTINGS
from database.schema.users import AuthTokenResponse, UserCreate, UserLogin
from services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _auth_response(auth: AuthTokenResponse, *, status_code: int) -> JSONResponse:
    response = JSONResponse(
        content=auth.model_dump(mode="json"),
        status_code=status_code,
    )
    max_age = int(SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES or 30) * 60
    response.set_cookie(
        key="access_token",
        value=auth.access_token,
        httponly=True,
        secure=SETTINGS.COOKIE_SECURE,
        samesite=SETTINGS.COOKIE_SAMESITE,
        max_age=max_age,
        path="/",
    )
    return response


@router.post(
    "/register",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    auth = auth_service.register(db, payload)
    return _auth_response(auth, status_code=status.HTTP_201_CREATED)


@router.post("/login", response_model=AuthTokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    auth = auth_service.login(db, payload)
    return _auth_response(auth, status_code=status.HTTP_200_OK)
