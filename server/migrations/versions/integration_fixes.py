"""Add body_fat to ProgressLog and rename calories_burned to calories

Revision ID: integration_fixes
Revises: 53a7361b2ff0
Create Date: 2025-11-26

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'integration_fixes'
down_revision = '53a7361b2ff0'
branch_labels = None
depends_on = None


def upgrade():
    # Add body_fat column to progress_logs table
    with op.batch_alter_table('progress_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body_fat', sa.Float(), nullable=True))
    
    # Rename calories_burned to calories in workouts table
    with op.batch_alter_table('workouts', schema=None) as batch_op:
        batch_op.alter_column('calories_burned',
                              new_column_name='calories',
                              existing_type=sa.Float(),
                              nullable=True)


def downgrade():
    # Rename calories back to calories_burned in workouts table
    with op.batch_alter_table('workouts', schema=None) as batch_op:
        batch_op.alter_column('calories',
                              new_column_name='calories_burned',
                              existing_type=sa.Float(),
                              nullable=True)
    
    # Remove body_fat column from progress_logs table
    with op.batch_alter_table('progress_logs', schema=None) as batch_op:
        batch_op.drop_column('body_fat')
