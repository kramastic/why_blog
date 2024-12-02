"""content Text

Revision ID: 251bc08b0109
Revises: 49c8dca0591b
Create Date: 2024-11-27 14:13:22.956612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '251bc08b0109'
down_revision: Union[str, None] = '49c8dca0591b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'content',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'content',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
