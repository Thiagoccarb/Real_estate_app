"""Add default admin user

Revision ID: 8733e48d3734
Revises: 2f9e7787ff43
Create Date: 2023-07-02 21:04:50.048791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8733e48d3734'
down_revision = '2f9e7787ff43'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the code to create the default admin user
    op.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES ('admin', 'user1234@gmail.com', '1234567abcd!T')
        """
    )

def downgrade() -> None:
    # Add the code to remove the default admin user
    op.execute(
        """
        DELETE FROM users WHERE username = 'admin'
        """
    )
