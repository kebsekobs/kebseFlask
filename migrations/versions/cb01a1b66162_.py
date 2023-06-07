"""empty message

Revision ID: cb01a1b66162
Revises: 692aad0f317a
Create Date: 2023-04-19 18:16:13.442715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb01a1b66162'
down_revision = '692aad0f317a'
branch_labels = None
depends_on = None


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('things in shops',
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.Column('thing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.ForeignKeyConstraint(['thing_id'], ['things.id'], )
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('things', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shop_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'shops', ['shop_id'], ['id'])

    op.drop_table('things in shops')
    # ### end Alembic commands ###
