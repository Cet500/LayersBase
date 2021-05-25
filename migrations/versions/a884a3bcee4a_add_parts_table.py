"""add parts table

Revision ID: a884a3bcee4a
Revises: f36a948dc2ea
Create Date: 2021-05-25 20:06:40.002553

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a884a3bcee4a'
down_revision = 'f36a948dc2ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('law_part',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_law', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=512), nullable=True),
    sa.ForeignKeyConstraint(['id_law'], ['law.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_law_part_title'), 'law_part', ['title'], unique=False)
    op.alter_column('law_article', 'name',
               existing_type=mysql.VARCHAR(length=512),
               nullable=True)
    op.alter_column('law_chapter', 'name',
               existing_type=mysql.VARCHAR(length=512),
               nullable=True)
    op.add_column('law_section', sa.Column('id_part', sa.Integer(), nullable=False))
    op.alter_column('law_section', 'name',
               existing_type=mysql.VARCHAR(length=512),
               nullable=True)
    op.drop_constraint('law_section_ibfk_1', 'law_section', type_='foreignkey')
    op.create_foreign_key(None, 'law_section', 'law_part', ['id_part'], ['id'])
    op.drop_column('law_section', 'id_law')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('law_section', sa.Column('id_law', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'law_section', type_='foreignkey')
    op.create_foreign_key('law_section_ibfk_1', 'law_section', 'law', ['id_law'], ['id'])
    op.alter_column('law_section', 'name',
               existing_type=mysql.VARCHAR(length=512),
               nullable=False)
    op.drop_column('law_section', 'id_part')
    op.alter_column('law_chapter', 'name',
               existing_type=mysql.VARCHAR(length=512),
               nullable=False)
    op.alter_column('law_article', 'name',
               existing_type=mysql.VARCHAR(length=512),
               nullable=False)
    op.drop_index(op.f('ix_law_part_title'), table_name='law_part')
    op.drop_table('law_part')
    # ### end Alembic commands ###