"""create_columns_bedrooms_bathrooms_description_on_table_properties

Revision ID: 2f9e7787ff43
Revises: 99ef78288eac
Create Date: 2023-04-10 22:43:57.119165

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "2f9e7787ff43"
down_revision = "99ef78288eac"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("properties", sa.Column("bedrooms", sa.Integer(), nullable=False))
    op.add_column("properties", sa.Column("bathrooms", sa.Integer(), nullable=False))
    op.add_column(
        "properties",
        sa.Column("description", mysql.VARCHAR(length=512), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("properties", "description")
    op.drop_column("properties", "bathrooms")
    op.drop_column("properties", "bedrooms")
    # ### end Alembic commands ###