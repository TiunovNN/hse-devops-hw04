"""Init tables.

Revision ID: ca79b727cd01
Revises: 
Create Date: 2023-10-28 15:31:07.034397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca79b727cd01'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dogs',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('kind', sa.Enum('terrier', 'bulldog', 'dalmatian', name='dogtype'), nullable=True),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_index(op.f('ix_dogs_pk'), 'dogs', ['pk'], unique=False)
    op.create_table('timestamps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_timestamps_id'), 'timestamps', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_timestamps_id'), table_name='timestamps')
    op.drop_table('timestamps')
    op.drop_index(op.f('ix_dogs_pk'), table_name='dogs')
    op.drop_table('dogs')
    # ### end Alembic commands ###
