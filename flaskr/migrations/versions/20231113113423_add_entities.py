"""Add entities

Revision ID: 293dfb332d93
Revises: 
Create Date: 2023-11-13 11:34:23.127355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '293dfb332d93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_name', sa.String(length=80), nullable=False),
    sa.Column('access_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token')
    )
    op.create_table('authorization_request',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authorization_request')
    op.drop_table('user')
    # ### end Alembic commands ###
