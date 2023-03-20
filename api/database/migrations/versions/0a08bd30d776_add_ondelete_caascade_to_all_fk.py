"""add_ondelete caascade to all fk

Revision ID: 0a08bd30d776
Revises: 5ff577e3c3ca
Create Date: 2023-03-19 22:16:18.460400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a08bd30d776'
down_revision = '5ff577e3c3ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('addresses_ibfk_1', 'addresses', type_='foreignkey')
    op.create_foreign_key(None, 'addresses', 'cities', ['city_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('images_ibfk_1', 'images', type_='foreignkey')
    op.create_foreign_key(None, 'images', 'properties', ['property_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('properties_ibfk_1', 'properties', type_='foreignkey')
    op.create_foreign_key(None, 'properties', 'addresses', ['address_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'properties', type_='foreignkey')
    op.create_foreign_key('properties_ibfk_1', 'properties', 'addresses', ['address_id'], ['id'])
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.create_foreign_key('images_ibfk_1', 'images', 'properties', ['property_id'], ['id'])
    op.drop_constraint(None, 'addresses', type_='foreignkey')
    op.create_foreign_key('addresses_ibfk_1', 'addresses', 'cities', ['city_id'], ['id'])
    # ### end Alembic commands ###
