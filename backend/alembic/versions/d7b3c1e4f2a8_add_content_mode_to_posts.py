"""add content_mode and rendered_content to posts

Revision ID: d7b3c1e4f2a8
Revises: c4f91e2a8b1d
Create Date: 2026-07-07 01:06:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "d7b3c1e4f2a8"
down_revision: Union[str, Sequence[str], None] = "c4f91e2a8b1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    contentmode = postgresql.ENUM(
        "markdown", "html", "blocks", name="contentmode", create_type=False
    )
    contentmode.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "posts",
        sa.Column(
            "content_mode",
            contentmode,
            nullable=False,
            server_default="html",
        ),
    )
    op.add_column("posts", sa.Column("rendered_content", sa.Text(), nullable=True))
    op.alter_column("posts", "content_mode", server_default=None)


def downgrade() -> None:
    op.drop_column("posts", "rendered_content")
    op.drop_column("posts", "content_mode")
    postgresql.ENUM(name="contentmode").drop(op.get_bind(), checkfirst=True)
