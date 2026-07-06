"""rename blocks content mode to components

Revision ID: f4a8c2d1e9b0
Revises: e8f2a1b9c3d0
Create Date: 2026-07-07 01:50:00.000000

"""

from typing import Sequence, Union

from alembic import op


revision: str = "f4a8c2d1e9b0"
down_revision: Union[str, Sequence[str], None] = "e8f2a1b9c3d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE contentmode RENAME VALUE 'blocks' TO 'components'")


def downgrade() -> None:
    op.execute("ALTER TYPE contentmode RENAME VALUE 'components' TO 'blocks'")
