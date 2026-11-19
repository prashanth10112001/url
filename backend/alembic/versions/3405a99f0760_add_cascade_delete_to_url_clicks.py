"""add cascade delete to url clicks

Revision ID: 3405a99f0760
Revises: 8000993c1c17
Create Date: 2026-11-17 17:13:22.783491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3405a99f0760'
down_revision: Union[str, Sequence[str], None] = '8000993c1c17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.drop_constraint(
        "url_clicks_url_id_fkey",
        "url_clicks",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "url_clicks_url_id_fkey",
        "url_clicks",
        "urls",
        ["url_id"],
        ["id"],
        ondelete="CASCADE"
    )

def downgrade():

    op.drop_constraint(
        "url_clicks_url_id_fkey",
        "url_clicks",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "url_clicks_url_id_fkey",
        "url_clicks",
        "urls",
        ["url_id"],
        ["id"]
    )
