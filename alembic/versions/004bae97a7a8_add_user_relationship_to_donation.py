"""Add user relationship to Donation

Revision ID: 004bae97a7a8
Revises: 2302438961dd
Create Date: 2022-11-14 08:23:19.274159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004bae97a7a8'
down_revision = '2302438961dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('fk_donation_user_id_user', 'donation', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_donation_user_id_user', 'donation', type_='foreignkey')
    # ### end Alembic commands ###
