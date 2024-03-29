"""empty message

Revision ID: 9850dd1732ed
Revises: 
Create Date: 2020-05-23 11:53:59.361208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9850dd1732ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action',
    sa.Column('id', sa.String(length=150), nullable=False),
    sa.Column('company_name', sa.String(length=150), nullable=False),
    sa.Column('company_full_name', sa.String(length=150), nullable=True),
    sa.Column('sector', sa.String(length=150), nullable=True),
    sa.Column('segment', sa.String(length=150), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('worker',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('actions_errors', sa.String(length=555), nullable=True),
    sa.Column('qnt_errors', sa.String(length=555), nullable=False),
    sa.Column('obs', sa.String(length=555), nullable=True),
    sa.Column('qnt_new_actions', sa.Integer(), nullable=False),
    sa.Column('qnt_update_quotation', sa.Integer(), nullable=False),
    sa.Column('qnt_update_indicators', sa.Integer(), nullable=False),
    sa.Column('qnt_update_balance', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('balance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.String(length=150), nullable=False),
    sa.Column('market_value', sa.Float(), nullable=True),
    sa.Column('company_value', sa.Float(), nullable=True),
    sa.Column('num_action', sa.Float(), nullable=True),
    sa.Column('assets', sa.Float(), nullable=True),
    sa.Column('current_assets', sa.Float(), nullable=True),
    sa.Column('availability', sa.Float(), nullable=True),
    sa.Column('gross_debt', sa.Float(), nullable=True),
    sa.Column('net_debt', sa.Float(), nullable=True),
    sa.Column('net_worth', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['action_id'], ['action.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('indicators',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.String(length=150), nullable=False),
    sa.Column('price_profit', sa.Float(), nullable=True),
    sa.Column('price_value_worth', sa.Float(), nullable=True),
    sa.Column('price_ebit', sa.Float(), nullable=True),
    sa.Column('price_net_revenueear', sa.Float(), nullable=True),
    sa.Column('price_active', sa.Float(), nullable=True),
    sa.Column('price_working_capital', sa.Float(), nullable=True),
    sa.Column('price_net_circle_active', sa.Float(), nullable=True),
    sa.Column('div_yield', sa.Float(), nullable=True),
    sa.Column('enterprise_value_ebitda', sa.Float(), nullable=True),
    sa.Column('enterprise_value_ebit', sa.Float(), nullable=True),
    sa.Column('revenue_growth_five_years', sa.Float(), nullable=True),
    sa.Column('profit_by_action', sa.Float(), nullable=True),
    sa.Column('patrimonial_value', sa.Float(), nullable=True),
    sa.Column('gross_margin', sa.Float(), nullable=True),
    sa.Column('ebit_margin', sa.Float(), nullable=True),
    sa.Column('net_margin', sa.Float(), nullable=True),
    sa.Column('ebit_active', sa.Float(), nullable=True),
    sa.Column('roic', sa.Float(), nullable=True),
    sa.Column('roe', sa.Float(), nullable=True),
    sa.Column('current_assets_liabilities', sa.Float(), nullable=True),
    sa.Column('debt_gross_patrimonial', sa.Float(), nullable=True),
    sa.Column('asset_turnover', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['action_id'], ['action.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quotas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_id', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['action_id'], ['action.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quotas')
    op.drop_table('indicators')
    op.drop_table('balance')
    op.drop_table('worker')
    op.drop_table('action')
    # ### end Alembic commands ###
