-- V026__notifications.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  body text,
  image text,
  action_url text,
  notification_type text,
  target_type text,
  target_id uuid,
  scheduled_at timestamptz,
  sent_at timestamptz,
  status text NOT NULL DEFAULT 'scheduled',
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- initial partition
CREATE TABLE IF NOT EXISTS public.notifications_2026 PARTITION OF public.notifications
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_notifications_status ON public.notifications (status);

COMMIT;
