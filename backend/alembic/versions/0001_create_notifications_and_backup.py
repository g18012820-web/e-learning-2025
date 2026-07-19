"""create notifications and backup tables

Revision ID: 0001_create_notifications_and_backup
Revises: 
Create Date: 2026-07-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

a_revision = '0001_create_notifications_and_backup'
revision = a_revision

down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')
    op.create_table(
        'notifications',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('template_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=False, server_default='in_app'),
        sa.Column('priority', sa.SmallInteger(), nullable=True, server_default='2'),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('channel', sa.String(length=50), nullable=True),
        sa.Column('target', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=True, server_default='pending'),
        sa.Column('scheduled_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('idx_notifications_scheduled_at', 'notifications', ['scheduled_at'])

    op.create_table(
        'notification_templates',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('channel', sa.String(length=30), nullable=False),
        sa.Column('title_template', sa.Text(), nullable=True),
        sa.Column('body_template', sa.Text(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('variables', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'notification_queue',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('notification_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('attempt', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('status', sa.String(length=30), nullable=True, server_default='queued'),
        sa.Column('next_try_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('idempotency_key', sa.Text(), nullable=True),
        sa.Column('worker_meta', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('last_attempt_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index('idx_queue_next_try', 'notification_queue', ['next_try_at'])
    op.create_index('idx_queue_status', 'notification_queue', ['status'])

    op.create_table(
        'notification_logs',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('notification_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('channel', sa.String(length=30), nullable=True),
        sa.Column('recipient', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=True),
        sa.Column('response', sa.JSON(), nullable=True),
        sa.Column('attempt', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('idx_logs_notification', 'notification_logs', ['notification_id'])

    op.create_table(
        'device_tokens',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('provider', sa.String(length=30), nullable=True),
        sa.Column('token', sa.Text(), nullable=True),
        sa.Column('platform', sa.String(length=30), nullable=True),
        sa.Column('meta', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('last_seen', sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_index('idx_device_user', 'device_tokens', ['user_id'])

    op.create_table(
        'backups',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('type', sa.String(length=30), nullable=True),
        sa.Column('storage', sa.String(length=30), nullable=True),
        sa.Column('size', sa.BigInteger(), nullable=True),
        sa.Column('checksum', sa.Text(), nullable=True),
        sa.Column('encrypted', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('status', sa.String(length=30), nullable=True, server_default='created'),
        sa.Column('started_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('finished_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_by', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'backup_files',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('backup_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('path', sa.Text(), nullable=True),
        sa.Column('size', sa.BigInteger(), nullable=True),
        sa.Column('checksum', sa.Text(), nullable=True),
    )

    op.create_table(
        'backup_logs',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('backup_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('level', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'notification_rules',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('trigger_type', sa.String(length=50), nullable=True),
        sa.Column('condition', sa.JSON(), nullable=True),
        sa.Column('actions', sa.JSON(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('priority', sa.Integer(), nullable=True, server_default='100'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'scheduled_notifications',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('notification_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('cron_expr', sa.Text(), nullable=True),
        sa.Column('timezone', sa.Text(), nullable=True),
        sa.Column('next_run', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'webhook_events',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('event_type', sa.Text(), nullable=True),
        sa.Column('target_url', sa.Text(), nullable=True),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('delivered', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('response', sa.JSON(), nullable=True),
        sa.Column('attempt', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('next_try', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('webhook_events')
    op.drop_table('scheduled_notifications')
    op.drop_table('notification_rules')
    op.drop_table('backup_logs')
    op.drop_table('backup_files')
    op.drop_table('backups')
    op.drop_index('idx_device_user', table_name='device_tokens')
    op.drop_table('device_tokens')
    op.drop_index('idx_logs_notification', table_name='notification_logs')
    op.drop_table('notification_logs')
    op.drop_index('idx_queue_status', table_name='notification_queue')
    op.drop_index('idx_queue_next_try', table_name='notification_queue')
    op.drop_table('notification_queue')
    op.drop_table('notification_templates')
    op.drop_index('idx_notifications_scheduled_at', table_name='notifications')
    op.drop_table('notifications'
    )
