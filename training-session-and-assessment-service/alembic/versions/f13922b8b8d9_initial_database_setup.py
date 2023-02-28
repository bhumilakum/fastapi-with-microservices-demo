"""initial database setup

Revision ID: f13922b8b8d9
Revises:
Create Date: 2023-02-27 22:23:14.051002

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f13922b8b8d9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column(
            "user_type",
            sa.Enum("admin", "mentor", "trainee", name="usertypeenum"),
            nullable=False,
        ),
        sa.Column(
            "created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_table(
        "training_session",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("total_time", sa.Integer(), nullable=True),
        sa.Column("user_fk", sa.Integer(), nullable=True),
        sa.Column("recording_link", sa.String(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("expected_attendees", sa.Integer(), nullable=True),
        sa.Column("present_attendees", sa.Integer(), nullable=True),
        sa.Column(
            "created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(["user_fk"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_training_session_id"), "training_session", ["id"], unique=False
    )
    op.create_table(
        "assignment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("related_session", sa.Integer(), nullable=True),
        sa.Column("given_date", sa.Date(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("total_score", sa.Float(), nullable=True),
        sa.Column("passing_score", sa.Float(), nullable=True),
        sa.Column(
            "created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["related_session"], ["training_session.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_assignment_id"), "assignment", ["id"], unique=False)
    op.create_table(
        "session_attendee",
        sa.Column("session_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_id"], ["training_session.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
    )
    op.create_table(
        "submission",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_fk", sa.Integer(), nullable=True),
        sa.Column("assignment_fk", sa.Integer(), nullable=True),
        sa.Column("submission_detail", sa.String(), nullable=True),
        sa.Column("submission_date", sa.Date(), nullable=True),
        sa.Column("obtained_score", sa.Float(), nullable=True),
        sa.Column(
            "result",
            sa.Enum("PASS", "FAIL", name="submissionresultenum"),
            nullable=True,
        ),
        sa.Column("submission_comment", sa.String(), nullable=True),
        sa.Column("mentor_remarks", sa.String(), nullable=True),
        sa.Column(
            "created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["assignment_fk"], ["assignment.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["user_fk"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_submission_id"), "submission", ["id"], unique=False)
    op.create_table(
        "grade",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("submission_fk", sa.Integer(), nullable=True),
        sa.Column("knowledge", sa.Float(), nullable=True),
        sa.Column("body_language", sa.Float(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("making_us_understand", sa.Float(), nullable=True),
        sa.Column("practical", sa.Float(), nullable=True),
        sa.Column(
            "created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["submission_fk"], ["submission.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_grade_id"), "grade", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_grade_id"), table_name="grade")
    op.drop_table("grade")
    op.drop_index(op.f("ix_submission_id"), table_name="submission")
    op.drop_table("submission")
    op.drop_table("session_attendee")
    op.drop_index(op.f("ix_assignment_id"), table_name="assignment")
    op.drop_table("assignment")
    op.drop_index(op.f("ix_training_session_id"), table_name="training_session")
    op.drop_table("training_session")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###