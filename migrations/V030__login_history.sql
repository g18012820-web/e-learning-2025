-- V030__login_history.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.login_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id),
  ip_address inet,
  device jsonb,
  success boolean,
  reason text,
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS public.login_history_2026 PARTITION OF public.login_history
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_login_history_user ON public.login_history (user_id);

COMMIT;
