"""baseline_initial

Revision ID: 0c0cb8fb5c79
Revises: 
Create Date: 2026-04-21 21:36:08.243189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c0cb8fb5c79'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
