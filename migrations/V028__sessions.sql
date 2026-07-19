-- V028__sessions.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  device_name text,
  device_model text,
  operating_system text,
  app_version text,
  ip_address inet,
  country text,
  city text,
  login_at timestamptz NOT NULL DEFAULT now(),
  last_activity timestamptz,
  status text NOT NULL DEFAULT 'active'
) PARTITION BY RANGE (login_at);

CREATE TABLE IF NOT EXISTS public.sessions_2026 PARTITION OF public.sessions
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_sessions_user ON public.sessions (user_id);

COMMIT;
