"""Add salon_id to users and description to salons

Revision ID: 20250929_153831
Revises: b8c19fe801a6
Create Date: 2024-12-19 15:38:31.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '20250929_153831'
down_revision = 'b8c19fe801a6'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add salon_id to users table and description to salons table.
    Using table recreation strategy for SQLite compatibility.
    """
    
    # First, add description to salons table
    # Create new salons table with description
    op.create_table('salons_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data from old salons table to new salons table
    op.execute(text("""
        INSERT INTO salons_new (id, uuid, name, address, created_at)
        SELECT id, uuid, name, address, created_at
        FROM salons
    """))
    
    # Drop old salons table
    op.drop_table('salons')
    
    # Rename new salons table
    op.rename_table('salons_new', 'salons')
    
    # Now, add salon_id to users table
    # Create new users table with salon_id
    op.create_table('users_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('CUSTOMER', 'ADMIN', 'MANAGER', 'STAFF', name='userrole'), nullable=False),
        sa.Column('salon_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['salon_id'], ['salons.id'], ),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Copy data from old users table to new users table
    op.execute(text("""
        INSERT INTO users_new (id, username, email, password_hash, role, created_at)
        SELECT id, username, email, password_hash, role, created_at
        FROM users
    """))
    
    # Drop old users table
    op.drop_table('users')
    
    # Rename new users table
    op.rename_table('users_new', 'users')


def downgrade():
    """
    Remove salon_id from users table and description from salons table.
    """
    
    # Remove salon_id from users table
    # Create new users table without salon_id
    op.create_table('users_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('CUSTOMER', 'ADMIN', 'MANAGER', 'STAFF', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Copy data from old users table to new users table (excluding salon_id)
    op.execute(text("""
        INSERT INTO users_new (id, username, email, password_hash, role, created_at)
        SELECT id, username, email, password_hash, role, created_at
        FROM users
    """))
    
    # Drop old users table
    op.drop_table('users')
    
    # Rename new users table
    op.rename_table('users_new', 'users')
    
    # Remove description from salons table
    # Create new salons table without description
    op.create_table('salons_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(length=36), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Copy data from old salons table to new salons table (excluding description)
    op.execute(text("""
        INSERT INTO salons_new (id, uuid, name, address, created_at)
        SELECT id, uuid, name, address, created_at
        FROM salons
    """))
    
    # Drop old salons table
    op.drop_table('salons')
    
    # Rename new salons table
    op.rename_table('salons_new', 'salons')
