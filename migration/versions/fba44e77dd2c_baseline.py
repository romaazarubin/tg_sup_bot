"""baseline

Revision ID: fba44e77dd2c
Revises: 
Create Date: 2022-10-07 22:27:29.978033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba44e77dd2c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'support_list',
        sa.Column('sup_name', sa.Text, nullable=False),
        sa.Column('sup_city', sa.Text, nullable=False)
    )
    op.create_table(
        'support_stats',
        sa.Column('support_name', sa.Text, nullable=False),
        sa.Column('user_name', sa.Text, nullable=False),
        sa.Column('city', sa.Text, nullable=False)
    )
    op.create_table(
        'us_id',
        sa.Column('user_id', sa.Text, nullable=False),
        sa.Column('city', sa.Text, nullable=False),
        sa.Column('message_id', sa.Text, nullable=False)
    )

def downgrade():
    op.drop_table('support_list')
    op.drop_table('support_stats')
    op.drop_table('us_id')