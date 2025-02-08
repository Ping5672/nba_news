# backend/alembic/versions/001_create_news_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('url', sa.String(255), nullable=False),
        sa.Column('image_url', sa.String(255)),
        sa.Column('published_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_published_at', 'news', ['published_at'])
    op.create_index('idx_title', 'news', ['title'])

def downgrade():
    op.drop_index('idx_published_at', 'news')
    op.drop_index('idx_title', 'news')
    op.drop_table('news')