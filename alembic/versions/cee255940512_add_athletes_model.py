"""add athletes model

Revision ID: cee255940512
Revises: 0b7fa4b4ac38
Create Date: 2025-07-01 11:53:22.522014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cee255940512'
down_revision: Union[str, Sequence[str], None] = '0b7fa4b4ac38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('athletes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('flow', sa.UUID(), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('dob', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('team', sa.String(length=255), nullable=True),
    sa.Column('coach', sa.String(length=255), nullable=True),
    sa.Column('is_group', sa.Integer(), nullable=True),
    sa.Column('fullkey', sa.String(length=255), nullable=True),
    sa.Column('start_n', sa.Integer(), nullable=True),
    sa.Column('pos', sa.Integer(), nullable=True),
    sa.Column('result', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_v7', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('pos_v1', sa.Integer(), nullable=True),
    sa.Column('pos_v2', sa.Integer(), nullable=True),
    sa.Column('pos_v3', sa.Integer(), nullable=True),
    sa.Column('pos_v4', sa.Integer(), nullable=True),
    sa.Column('pos_v5', sa.Integer(), nullable=True),
    sa.Column('pos_v6', sa.Integer(), nullable=True),
    sa.Column('pos_v7', sa.Integer(), nullable=True),
    sa.Column('subresult', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('penalty', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('post', sa.String(length=255), nullable=True),
    sa.Column('v1', sa.Integer(), nullable=True),
    sa.Column('v2', sa.Integer(), nullable=True),
    sa.Column('v3', sa.Integer(), nullable=True),
    sa.Column('v4', sa.Integer(), nullable=True),
    sa.Column('checked', sa.Boolean(), nullable=False),
    sa.Column('music_1', sa.String(length=255), nullable=True),
    sa.Column('music_2', sa.String(length=255), nullable=True),
    sa.Column('music_3', sa.String(length=255), nullable=True),
    sa.Column('music_4', sa.String(length=255), nullable=True),
    sa.Column('music_5', sa.String(length=255), nullable=True),
    sa.Column('music_6', sa.String(length=255), nullable=True),
    sa.Column('music_7', sa.String(length=255), nullable=True),
    sa.Column('performed', sa.Boolean(), nullable=False),
    sa.Column('ofp', sa.Boolean(), nullable=False),
    sa.Column('result_ofp1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp7', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp8', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp9', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp10', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp11', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp12', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp13', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp14', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_ofp15', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_tv', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_av', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_ex', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_pred', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_pred_pos', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_tv_f', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_av_f', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_ex_f', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_final', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_est_final_pos', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('est', sa.Boolean(), nullable=False),
    sa.Column('aer', sa.Boolean(), nullable=False),
    sa.Column('result_aer_e1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_e2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_e3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_e4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_e5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_e6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_d1d2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('penalty_aer_dd', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('penalty_aer_cjp', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('penalty_aer_l', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_e', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_a', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer_d', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('penalty_aer', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('result_aer', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_d_v7', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_a_v7', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v1', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v2', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v3', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v4', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v5', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v6', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('total_e_v7', sa.Numeric(precision=100, scale=7), nullable=True),
    sa.Column('man', sa.Boolean(), nullable=False),
    sa.Column('kat', sa.Boolean(), nullable=False),
    sa.Column('kat_1_res_0', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_res_1', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_res_2', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_res_3', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_res_4', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_res_0', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_res_1', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_res_2', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_res_3', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_res_4', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_res_0', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_res_1', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_res_2', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_res_3', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_res_4', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_res', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_res', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_res', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_2_res', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_2_pos', sa.Integer(), nullable=True),
    sa.Column('kat_f_pos', sa.Integer(), nullable=True),
    sa.Column('kat_1_min', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_1_max', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_min', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_2_max', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_min', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_f_max', sa.Numeric(precision=100, scale=2), nullable=True),
    sa.Column('kat_type', sa.Integer(), nullable=True),
    sa.Column('kat_flag1', sa.Integer(), nullable=True),
    sa.Column('kat_flag2', sa.Integer(), nullable=True),
    sa.Column('kat_1_min_n', sa.Integer(), nullable=True),
    sa.Column('kat_1_max_n', sa.Integer(), nullable=True),
    sa.Column('kat_2_min_n', sa.Integer(), nullable=True),
    sa.Column('kat_2_max_n', sa.Integer(), nullable=True),
    sa.Column('kat_f_min_n', sa.Integer(), nullable=True),
    sa.Column('kat_f_max_n', sa.Integer(), nullable=True),
    sa.Column('art', sa.Boolean(), nullable=False),
    sa.Column('art_boy', sa.Boolean(), nullable=False),
    sa.Column('art_vk', sa.Boolean(), nullable=False),
    sa.Column('medal', sa.Boolean(), nullable=False),
    sa.Column('v5', sa.Integer(), nullable=True),
    sa.Column('v6', sa.Integer(), nullable=True),
    sa.Column('is_group_type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['flow'], ['flows.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('athletes')
    # ### end Alembic commands ###
