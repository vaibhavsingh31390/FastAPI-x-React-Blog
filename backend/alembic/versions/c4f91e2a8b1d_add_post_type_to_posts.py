"""add post_type column to posts

Revision ID: c4f91e2a8b1d
Revises: 8a12a74f2b9d
Create Date: 2026-07-07 01:02:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c4f91e2a8b1d"
down_revision: Union[str, Sequence[str], None] = "8a12a74f2b9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    posttype = postgresql.ENUM("post", "page", name="posttype", create_type=False)
    posttype.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "posts",
        sa.Column(
            "post_type",
            posttype,
            nullable=False,
            server_default="post",
        ),
    )
    op.alter_column("posts", "post_type", server_default=None)


def downgrade() -> None:
    op.drop_column("posts", "post_type")
    postgresql.ENUM(name="posttype").drop(op.get_bind(), checkfirst=True)
