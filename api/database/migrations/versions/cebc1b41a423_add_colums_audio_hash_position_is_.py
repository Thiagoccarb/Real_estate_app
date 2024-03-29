"""add_colums_audio_hash_position_is_active_in_images_table

Revision ID: cebc1b41a423
Revises: 0a08bd30d776
Create Date: 2023-03-26 00:21:18.627809

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "cebc1b41a423"
down_revision = "0a08bd30d776"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "images", sa.Column("audio_hash", mysql.VARCHAR(length=512), nullable=True)
    )
    op.add_column("images", sa.Column("position", sa.Integer(), nullable=True))
    op.add_column("images", sa.Column("is_active", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("images", "is_active")
    op.drop_column("images", "position")
    op.drop_column("images", "audio_hash")
    # ### end Alembic commands ###
