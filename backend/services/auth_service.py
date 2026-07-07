from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.users import User
from database.schema.users import AuthTokenResponse, UserCreate, UserLogin, UsersSchema
from repositories import user_repo
from utils.auth_utils import create_jwt


def _build_auth_response(user: User) -> AuthTokenResponse:
    token = create_jwt({"sub": str(user.id)})
    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        user=UsersSchema.model_validate(user),
    )


def register(db: Session, payload: UserCreate) -> AuthTokenResponse:
    existing_user = user_repo.get_by_email(db, payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = user_repo.create(db, payload)
    return _build_auth_response(user)


def login(db: Session, payload: UserLogin) -> AuthTokenResponse:
    user = user_repo.get_by_email(db, payload.email)
    if user is None or not user_repo.verify_password(
        payload.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )
    return _build_auth_response(user)
