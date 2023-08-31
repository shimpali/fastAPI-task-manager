"""create_main_tables

Revision ID: dc7cc3be7175
Revises: 
Create Date: 2023-08-31 12:36:45.297582

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'dc7cc3be7175'
down_revision = None
branch_labels = None
depends_on = None


def create_tasks_table() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.Text, nullable=False, index=True),
        sa.Column("status", sa.Text, nullable=False, server_default="not_started"),
    )


def upgrade() -> None:
    create_tasks_table()


def downgrade() -> None:
    op.drop_table("tasks")
