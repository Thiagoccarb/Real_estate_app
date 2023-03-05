"""create_table_properties

Revision ID: 95009367700f
Revises:
Create Date: 2023-02-25 22:55:47.028194

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "95009367700f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "properties",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", mysql.VARCHAR(length=45), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("properties")
