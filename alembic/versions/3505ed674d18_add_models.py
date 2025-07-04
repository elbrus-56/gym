"""add models

Revision ID: 3505ed674d18
Revises: ae97d60c81c0
Create Date: 2025-07-01 11:07:39.850623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3505ed674d18'
down_revision: Union[str, Sequence[str], None] = 'ae97d60c81c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('age_from', sa.String(length=10), nullable=True),
    sa.Column('age_to', sa.String(length=10), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('vid', sa.String(length=50), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('hour_from', sa.String(length=10), nullable=True),
    sa.Column('min_from', sa.String(length=10), nullable=True),
    sa.Column('hour_to', sa.String(length=10), nullable=True),
    sa.Column('min_to', sa.String(length=255), nullable=True),
    sa.Column('fullname', sa.String(length=255), nullable=True),
    sa.Column('group', sa.SmallInteger(), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=True),
    sa.Column('fullkey', sa.String(length=255), nullable=True),
    sa.Column('wa', sa.String(length=10), nullable=True),
    sa.Column('prog', sa.String(length=255), nullable=True),
    sa.Column('brake_type', sa.SmallInteger(), nullable=True),
    sa.Column('brake_name', sa.String(length=255), nullable=True),
    sa.Column('ex', sa.Integer(), nullable=True),
    sa.Column('sec', sa.Integer(), nullable=True),
    sa.Column('letter', sa.String(length=255), nullable=True),
    sa.Column('v1', sa.SmallInteger(), nullable=True),
    sa.Column('v2', sa.SmallInteger(), nullable=True),
    sa.Column('v3', sa.SmallInteger(), nullable=True),
    sa.Column('v4', sa.SmallInteger(), nullable=True),
    sa.Column('vert', sa.SmallInteger(), nullable=True),
    sa.Column('num_sf', sa.SmallInteger(), nullable=True),
    sa.Column('min_sf', sa.SmallInteger(), nullable=True),
    sa.Column('team_k', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('max_d', sa.Integer(), nullable=True),
    sa.Column('ofp', sa.Boolean(), nullable=True),
    sa.Column('ofp_n', sa.SmallInteger(), nullable=True),
    sa.Column('ofp_ex1', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex2', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex3', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex4', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex5', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex6', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex7', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex8', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex9', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex10', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex11', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex12', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex13', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex14', sa.String(length=255), nullable=True),
    sa.Column('ofp_ex15', sa.String(length=255), nullable=True),
    sa.Column('est', sa.Boolean(), nullable=True),
    sa.Column('est_gr', sa.SmallInteger(), nullable=True),
    sa.Column('est_short', sa.SmallInteger(), nullable=True),
    sa.Column('aer', sa.Boolean(), nullable=True),
    sa.Column('aer_cat', sa.SmallInteger(), nullable=True),
    sa.Column('aer_age', sa.SmallInteger(), nullable=True),
    sa.Column('aer_sex', sa.SmallInteger(), nullable=True),
    sa.Column('aer_dd_k', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('aer_year', sa.String(length=255), nullable=True),
    sa.Column('aer_final', sa.Boolean(), nullable=True),
    sa.Column('man', sa.Boolean(), nullable=True),
    sa.Column('man_cat', sa.SmallInteger(), nullable=True),
    sa.Column('kat', sa.Boolean(), nullable=True),
    sa.Column('kat_type', sa.SmallInteger(), nullable=True),
    sa.Column('kat_age', sa.SmallInteger(), nullable=True),
    sa.Column('kat_sex', sa.SmallInteger(), nullable=True),
    sa.Column('kat_ex', sa.SmallInteger(), nullable=True),
    sa.Column('kat_name', sa.String(length=255), nullable=True),
    sa.Column('kat_kata_name1', sa.String(length=255), nullable=True),
    sa.Column('kat_kata_name2', sa.String(length=255), nullable=True),
    sa.Column('kat_kata_name3', sa.String(length=255), nullable=True),
    sa.Column('kat_kata_ind1', sa.SmallInteger(), nullable=True),
    sa.Column('kat_kata_ind2', sa.SmallInteger(), nullable=True),
    sa.Column('kat_kata_ind3', sa.SmallInteger(), nullable=True),
    sa.Column('art', sa.Boolean(), nullable=True),
    sa.Column('art_man', sa.Boolean(), nullable=True),
    sa.Column('art_age_number', sa.Integer(), nullable=True),
    sa.Column('art_age_name', sa.String(length=255), nullable=True),
    sa.Column('art_type', sa.Boolean(), nullable=True),
    sa.Column('art_grade_number', sa.Integer(), nullable=True),
    sa.Column('art_grade_name', sa.String(length=255), nullable=True),
    sa.Column('art_fig', sa.Boolean(), nullable=True),
    sa.Column('v5', sa.SmallInteger(), nullable=True),
    sa.Column('v6', sa.SmallInteger(), nullable=True),
    sa.Column('group_type', sa.SmallInteger(), nullable=True),
    sa.Column('age_group_num', sa.SmallInteger(), nullable=True),
    sa.Column('age_group_name', sa.String(length=255), nullable=True),
    sa.Column('step_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('periods',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('value', sa.String(length=20), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('hour_from', sa.String(length=10), nullable=True),
    sa.Column('min_from', sa.String(length=10), nullable=True),
    sa.Column('hour_to', sa.String(length=10), nullable=True),
    sa.Column('min_to', sa.String(length=10), nullable=True),
    sa.Column('age_from', sa.String(length=10), nullable=True),
    sa.Column('age_to', sa.String(length=10), nullable=True),
    sa.Column('fullkey', sa.String(length=255), nullable=True),
    sa.Column('n', sa.SmallInteger(), nullable=True),
    sa.Column('art', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.add_column('competitions', sa.Column('skip_pos', sa.Boolean(), nullable=True))
    op.add_column('competitions', sa.Column('check_ead', sa.Boolean(), nullable=True))
    op.add_column('competitions', sa.Column('art', sa.Boolean(), nullable=True))
    op.add_column('competitions', sa.Column('final', sa.Boolean(), nullable=True))
    op.add_column('competitions', sa.Column('key', sa.String(length=255), nullable=True))
    op.add_column('competitions', sa.Column('team_type', sa.Boolean(), nullable=True))
    op.add_column('competitions', sa.Column('team_n', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'competitions', ['key'])
    op.add_column('flows', sa.Column('name', sa.String(length=255), nullable=True))
    op.alter_column('flows', 'min_to',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=10),
               existing_nullable=True)
    op.alter_column('flows', 'key',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.create_unique_constraint(None, 'flows', ['key'])
    op.drop_column('flows', 'team_k')
    op.drop_column('flows', 'aer_sex')
    op.drop_column('flows', 'age_group_num')
    op.drop_column('flows', 'kat_kata_ind2')
    op.drop_column('flows', 'art_fig')
    op.drop_column('flows', 'aer_age')
    op.drop_column('flows', 'age_to')
    op.drop_column('flows', 'kat_sex')
    op.drop_column('flows', 'ofp_ex8')
    op.drop_column('flows', 'kat_age')
    op.drop_column('flows', 'letter')
    op.drop_column('flows', 'aer_final')
    op.drop_column('flows', 'art_type')
    op.drop_column('flows', 'kat_kata_name1')
    op.drop_column('flows', 'ex')
    op.drop_column('flows', 'v3')
    op.drop_column('flows', 'ofp_ex5')
    op.drop_column('flows', 'group_type')
    op.drop_column('flows', 'kat_ex')
    op.drop_column('flows', 'ofp')
    op.drop_column('flows', 'kat_name')
    op.drop_column('flows', 'kat')
    op.drop_column('flows', 'ofp_ex7')
    op.drop_column('flows', 'date')
    op.drop_column('flows', 'est')
    op.drop_column('flows', 'category')
    op.drop_column('flows', 'aer_dd_k')
    op.drop_column('flows', 'max_d')
    op.drop_column('flows', 'kat_type')
    op.drop_column('flows', 'vid')
    op.drop_column('flows', 'ofp_ex1')
    op.drop_column('flows', 'ofp_ex10')
    op.drop_column('flows', 'ofp_ex11')
    op.drop_column('flows', 'man')
    op.drop_column('flows', 'v4')
    op.drop_column('flows', 'v1')
    op.drop_column('flows', 'kat_kata_name3')
    op.drop_column('flows', 'prog')
    op.drop_column('flows', 'aer_cat')
    op.drop_column('flows', 'art_age_number')
    op.drop_column('flows', 'kat_kata_name2')
    op.drop_column('flows', 'est_short')
    op.drop_column('flows', 'ofp_ex14')
    op.drop_column('flows', 'v5')
    op.drop_column('flows', 'art')
    op.drop_column('flows', 'wa')
    op.drop_column('flows', 'ofp_ex3')
    op.drop_column('flows', 'aer_year')
    op.drop_column('flows', 'ofp_ex6')
    op.drop_column('flows', 'ofp_ex13')
    op.drop_column('flows', 'sec')
    op.drop_column('flows', 'art_grade_name')
    op.drop_column('flows', 'man_cat')
    op.drop_column('flows', 'age_group_name')
    op.drop_column('flows', 'kat_kata_ind1')
    op.drop_column('flows', 'art_age_name')
    op.drop_column('flows', 'ofp_ex2')
    op.drop_column('flows', 'art_grade_number')
    op.drop_column('flows', 'ofp_ex15')
    op.drop_column('flows', 'group')
    op.drop_column('flows', 'est_gr')
    op.drop_column('flows', 'ofp_n')
    op.drop_column('flows', 'kat_kata_ind3')
    op.drop_column('flows', 'ofp_ex4')
    op.drop_column('flows', 'ofp_ex12')
    op.drop_column('flows', 'age_from')
    op.drop_column('flows', 'min_sf')
    op.drop_column('flows', 'step_name')
    op.drop_column('flows', 'num_sf')
    op.drop_column('flows', 'vert')
    op.drop_column('flows', 'aer')
    op.drop_column('flows', 'ofp_ex9')
    op.drop_column('flows', 'v2')
    op.drop_column('flows', 'art_man')
    op.drop_column('flows', 'v6')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flows', sa.Column('v6', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_man', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('v2', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex9', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('vert', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('num_sf', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('step_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('min_sf', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('age_from', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex12', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex4', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_kata_ind3', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_n', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('est_gr', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('group', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex15', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_grade_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex2', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_age_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_kata_ind1', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('age_group_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('man_cat', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_grade_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('sec', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex13', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex6', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer_year', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex3', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('wa', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('v5', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex14', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('est_short', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_kata_name2', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_age_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer_cat', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('prog', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_kata_name3', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('v1', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('v4', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('man', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex11', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex10', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex1', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('vid', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_type', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('max_d', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer_dd_k', sa.NUMERIC(precision=100, scale=7), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('category', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('est', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex7', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_ex', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('group_type', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex5', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('v3', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ex', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_kata_name1', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_type', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer_final', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('letter', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_age', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('ofp_ex8', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_sex', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('age_to', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer_age', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('art_fig', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('kat_kata_ind2', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('age_group_num', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('aer_sex', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('flows', sa.Column('team_k', sa.NUMERIC(precision=100, scale=7), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'flows', type_='unique')
    op.alter_column('flows', 'key',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('flows', 'min_to',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    op.drop_column('flows', 'name')
    op.drop_constraint(None, 'competitions', type_='unique')
    op.drop_column('competitions', 'team_n')
    op.drop_column('competitions', 'team_type')
    op.drop_column('competitions', 'key')
    op.drop_column('competitions', 'final')
    op.drop_column('competitions', 'art')
    op.drop_column('competitions', 'check_ead')
    op.drop_column('competitions', 'skip_pos')
    op.drop_table('periods')
    op.drop_table('groups')
    # ### end Alembic commands ###
