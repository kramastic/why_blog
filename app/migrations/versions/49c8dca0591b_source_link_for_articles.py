"""source_link for articles

Revision ID: 49c8dca0591b
Revises: 74bb0c2da650
Create Date: 2024-11-23 13:19:24.058281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49c8dca0591b'
down_revision: Union[str, None] = '74bb0c2da650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('source_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'source_link')
    # ### end Alembic commands ###
