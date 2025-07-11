"""initial migration

Revision ID: 010f78e389a0
Revises: 
Create Date: 2025-06-27 13:39:56.797438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '010f78e389a0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('competitions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('fullname', sa.String(length=255), nullable=True),
    sa.Column('age_from', sa.String(length=10), nullable=True),
    sa.Column('age_to', sa.String(length=10), nullable=True),
    sa.Column('organizer', sa.String(length=255), nullable=True),
    sa.Column('judge', sa.String(length=255), nullable=True),
    sa.Column('info', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('PLANNED', 'ACTIVE', 'COMPLETED', name='competitionstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('competitions')
    # ### end Alembic commands ###
