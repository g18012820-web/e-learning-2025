-- Initial SQL migrations for notifications, queue, logs, device tokens and backup tables

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  template_id uuid,
  title text,
  body text,
  type varchar(50) NOT NULL DEFAULT 'in_app',
  priority smallint DEFAULT 2,
  payload jsonb,
  channel varchar(50),
  target jsonb,
  status varchar(30) DEFAULT 'pending',
  scheduled_at timestamptz,
  created_by uuid,
  created_at timestamptz DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notifications_scheduled_at ON notifications(scheduled_at);

CREATE TABLE IF NOT EXISTS notification_templates (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  channel varchar(30) NOT NULL,
  title_template text,
  body_template text,
  metadata jsonb,
  variables jsonb,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS notification_queue (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  notification_id uuid,
  attempt integer DEFAULT 0,
  status varchar(30) DEFAULT 'queued',
  next_try_at timestamptz,
  idempotency_key text,
  worker_meta jsonb,
  created_at timestamptz DEFAULT now(),
  last_attempt_at timestamptz
);
CREATE INDEX IF NOT EXISTS idx_queue_next_try ON notification_queue(next_try_at);
CREATE INDEX IF NOT EXISTS idx_queue_status ON notification_queue(status);

CREATE TABLE IF NOT EXISTS notification_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  notification_id uuid,
  channel varchar(30),
  recipient text,
  status varchar(30),
  response jsonb,
  attempt integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_logs_notification ON notification_logs(notification_id);

CREATE TABLE IF NOT EXISTS device_tokens (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid,
  provider varchar(30),
  token text,
  platform varchar(30),
  meta jsonb,
  created_at timestamptz DEFAULT now(),
  last_seen timestamptz
);
CREATE INDEX IF NOT EXISTS idx_device_user ON device_tokens(user_id);

-- Backup tables
CREATE TABLE IF NOT EXISTS backups (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text,
  type varchar(30), -- full/incremental/differential
  storage varchar(30),
  size bigint,
  checksum text,
  encrypted boolean DEFAULT false,
  status varchar(30) DEFAULT 'created',
  started_at timestamptz,
  finished_at timestamptz,
  created_by uuid,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS backup_files (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  backup_id uuid,
  path text,
  size bigint,
  checksum text
);

CREATE TABLE IF NOT EXISTS backup_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  backup_id uuid,
  message text,
  level varchar(20),
  created_at timestamptz DEFAULT now()
);

-- Scheduled notifications and rules
CREATE TABLE IF NOT EXISTS notification_rules (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text,
  trigger_type varchar(50),
  condition jsonb,
  actions jsonb,
  active boolean DEFAULT true,
  priority integer DEFAULT 100,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scheduled_notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  notification_id uuid,
  cron_expr text,
  timezone text,
  next_run timestamptz,
  active boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

-- Webhook events
CREATE TABLE IF NOT EXISTS webhook_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type text,
  target_url text,
  payload jsonb,
  delivered boolean DEFAULT false,
  response jsonb,
  attempt integer DEFAULT 0,
  next_try timestamptz,
  created_at timestamptz DEFAULT now()
);
