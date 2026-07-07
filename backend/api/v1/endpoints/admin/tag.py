from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.tags import TagCreate, TagSchema, TagUpdate
from services import tag_service

# Add dependencies=[Depends(get_current_admin)] when auth middleware is ready.
router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
    return tag_service.create_tag(db, payload)


@router.patch("/{tag_id}", response_model=TagSchema)
def update_tag(
    tag_id: int,
    payload: TagUpdate,
    db: Session = Depends(get_db),
):
    return tag_service.update_tag(db, tag_id, payload)


@router.delete("/{tag_id}", response_model=TagSchema)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    return tag_service.delete_tag(db, tag_id)
