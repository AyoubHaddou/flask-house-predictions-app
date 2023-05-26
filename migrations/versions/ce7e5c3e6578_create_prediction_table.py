"""create prediction table

Revision ID: ce7e5c3e6578
Revises: 
Create Date: 2022-11-14 22:54:14.912098

"""
from alembic import op
import sqlalchemy as sa

import datetime 
# revision identifiers, used by Alembic.
revision = 'ce7e5c3e6578'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Prediction',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('created_on', sa.DateTime, default=datetime.date.today()),
        sa.Column('overall_qual', sa.Integer),
        sa.Column('neighborhood', sa.String),
        sa.Column('ms_subclass', sa.String),
        sa.Column('gr_liv_area', sa.String),
        sa.Column('misc_val', sa.Integer),
        sa.Column('kitchen_qual', sa.String),
        sa.Column('bsmtfin_sf_1', sa.Integer),
        sa.Column('garage_cars', sa.Integer),
        sa.Column('overall_cond', sa.Integer),
        sa.Column('exter_qual', sa.String),
        sa.Column('price', sa.Integer),
    )



def downgrade() -> None:
    op.drop_table('Prediction')
