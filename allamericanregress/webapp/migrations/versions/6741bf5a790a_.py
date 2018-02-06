"""empty message

Revision ID: 6741bf5a790a
Revises: 
Create Date: 2018-01-30 00:07:38.253122

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6741bf5a790a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('path', sa.String(), nullable=True),
                    sa.Column('command', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('log', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('program', sa.Integer(), nullable=True),
                    sa.Column('output', sa.String(), nullable=True),
                    sa.Column('exit_code', sa.Integer(), nullable=True),
                    sa.Column('date', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['program'],
                        ['program.id'],
                    ), sa.PrimaryKeyConstraint('id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    op.drop_table('program')
    # ### end Alembic commands ###
