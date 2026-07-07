from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.category import CategoryCreate, CategorySchema, CategoryUpdate
from services import category_service

# Add dependencies=[Depends(get_current_admin)] when auth middleware is ready.
router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, payload)


@router.patch("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
):
    return category_service.update_category(db, category_id, payload)


@router.delete("/{category_id}", response_model=CategorySchema)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.delete_category(db, category_id)
