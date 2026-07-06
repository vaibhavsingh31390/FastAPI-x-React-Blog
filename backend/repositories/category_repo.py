from typing import Literal

from sqlalchemy.orm import Session, selectinload

from database.models.category import Category
from database.schema.category import CategoryCreate, CategoryUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Category]:
    order = Category.created_at.desc() if sort == "desc" else Category.created_at.asc()
    return db.query(Category).order_by(order).offset(skip).limit(limit).all()


def get_by_id(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_by_slug(db: Session, slug: str) -> Category | None:
    return db.query(Category).filter(Category.slug == slug).first()


def create(db: Session, category_in: CategoryCreate) -> Category:
    db_category = Category(
        slug=category_in.slug,
        name=category_in.name,
        description=category_in.description,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update(db: Session, db_category: Category, category_in: CategoryUpdate) -> Category:
    update_data = category_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete(db: Session, db_category: Category) -> Category:
    db.delete(db_category)
    db.commit()
    return db_category


def get_by_id_with_posts(db: Session, category_id: int) -> Category | None:
    return (
        db.query(Category)
        .options(selectinload(Category.posts))
        .filter(Category.id == category_id)
        .first()
    )


def get_by_slug_with_posts(db: Session, slug: str) -> Category | None:
    return (
        db.query(Category)
        .options(selectinload(Category.posts))
        .filter(Category.slug == slug)
        .first()
    )
