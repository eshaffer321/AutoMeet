"""Add duration to recording

Revision ID: 7a18af11473e
Revises: 2516ad344c50
Create Date: 2025-03-29 06:24:17.795873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a18af11473e'
down_revision: Union[str, None] = '2516ad344c50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recording', sa.Column('duration', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recording', 'duration')
    # ### end Alembic commands ###
