"""change title_article

Revision ID: 505eb1d6adce
Revises: ddd0efd1153f
Create Date: 2024-11-23 12:49:43.789062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '505eb1d6adce'
down_revision: Union[str, None] = 'ddd0efd1153f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'title',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'title',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    # ### end Alembic commands ###
