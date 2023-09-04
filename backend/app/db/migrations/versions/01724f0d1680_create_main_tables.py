"""create_main_tables

Revision ID: 01724f0d1680
Revises: 
Create Date: 2023-09-02 14:12:42.725726

"""
from alembic import op
import sqlalchemy as sa

from app.models.project import ProjectStatus

# revision identifiers, used by Alembic
revision = '01724f0d1680'
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


def create_projects_table() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("created_date", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("due_date", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("status", sa.Enum(ProjectStatus), nullable=False, server_default=ProjectStatus.not_started),
    )


def upgrade() -> None:
    create_tasks_table()
    create_projects_table()


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("projects")