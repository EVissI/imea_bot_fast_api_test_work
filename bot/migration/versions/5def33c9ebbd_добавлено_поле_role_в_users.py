"""Добавлено поле role в users

Revision ID: 5def33c9ebbd
Revises: 1d38cea65046
Create Date: 2025-02-01 04:22:09.955192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5def33c9ebbd'
down_revision: Union[str, None] = '1d38cea65046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.Enum('Admin', 'User', name='role'), server_default='User', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
