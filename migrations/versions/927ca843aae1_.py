"""empty message

Revision ID: 927ca843aae1
Revises: 
Create Date: 2019-06-28 16:22:45.992623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '927ca843aae1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('role', sa.String(length=120), nullable=False),
    sa.Column('created_by', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fullname')
    )
    op.create_table('dustbin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dustbin_name', sa.String(length=20), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('location', sa.Text(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['users_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dustbin')
    op.drop_table('user')
    # ### end Alembic commands ###
