-- V031__activity_logs.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.activity_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid,
  action text NOT NULL,
  details jsonb,
  ip_address inet,
  device jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS public.activity_logs_2026 PARTITION OF public.activity_logs
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_activity_logs_user ON public.activity_logs (user_id);
CREATE INDEX IF NOT EXISTS ix_activity_logs_action ON public.activity_logs (action);

COMMIT;
