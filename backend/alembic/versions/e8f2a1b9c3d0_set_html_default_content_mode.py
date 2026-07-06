"""set html as default content_mode

Revision ID: e8f2a1b9c3d0
Revises: d7b3c1e4f2a8
Create Date: 2026-07-07 01:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = "e8f2a1b9c3d0"
down_revision: Union[str, Sequence[str], None] = "d7b3c1e4f2a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("posts", "content_mode", server_default="html")


def downgrade() -> None:
    op.alter_column("posts", "content_mode", server_default="markdown")
