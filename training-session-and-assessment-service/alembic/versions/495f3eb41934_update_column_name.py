"""update column name

Revision ID: 495f3eb41934
Revises: 672186f61222
Create Date: 2023-03-10 18:30:40.806853

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "495f3eb41934"
down_revision = "672186f61222"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("grade", sa.Column("submission_id", sa.Integer(), nullable=True))
    op.drop_constraint("grade_submission_fk_fkey", "grade", type_="foreignkey")
    op.create_foreign_key(
        None, "grade", "submission", ["submission_id"], ["id"], ondelete="SET NULL"
    )
    op.drop_column("grade", "submission_fk")
    op.add_column("submission", sa.Column("user_id", sa.Integer(), nullable=True))
    op.add_column("submission", sa.Column("assignment_id", sa.Integer(), nullable=True))
    op.drop_constraint("submission_user_fk_fkey", "submission", type_="foreignkey")
    op.drop_constraint(
        "submission_assignment_fk_fkey", "submission", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "submission", "assignment", ["assignment_id"], ["id"], ondelete="SET NULL"
    )
    op.create_foreign_key(
        None, "submission", "users", ["user_id"], ["id"], ondelete="SET NULL"
    )
    op.drop_column("submission", "user_fk")
    op.drop_column("submission", "assignment_fk")
    op.add_column("training_session", sa.Column("user_id", sa.Integer(), nullable=True))
    op.drop_constraint(
        "training_session_user_fk_fkey", "training_session", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "training_session", "users", ["user_id"], ["id"], ondelete="SET NULL"
    )
    op.drop_column("training_session", "user_fk")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "training_session",
        sa.Column("user_fk", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "training_session", type_="foreignkey")
    op.create_foreign_key(
        "training_session_user_fk_fkey",
        "training_session",
        "users",
        ["user_fk"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("training_session", "user_id")
    op.add_column(
        "submission",
        sa.Column("assignment_fk", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "submission",
        sa.Column("user_fk", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "submission", type_="foreignkey")
    op.drop_constraint(None, "submission", type_="foreignkey")
    op.create_foreign_key(
        "submission_assignment_fk_fkey",
        "submission",
        "assignment",
        ["assignment_fk"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "submission_user_fk_fkey",
        "submission",
        "users",
        ["user_fk"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("submission", "assignment_id")
    op.drop_column("submission", "user_id")
    op.add_column(
        "grade",
        sa.Column("submission_fk", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "grade", type_="foreignkey")
    op.create_foreign_key(
        "grade_submission_fk_fkey",
        "grade",
        "submission",
        ["submission_fk"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("grade", "submission_id")
    # ### end Alembic commands ###
