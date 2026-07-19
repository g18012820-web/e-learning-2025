-- V032__audit_logs.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.audit_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_user_id uuid,
  target_table text,
  target_id uuid,
  action text,
  diff jsonb,
  metadata jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS public.audit_logs_2026 PARTITION OF public.audit_logs
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_audit_logs_actor ON public.audit_logs (actor_user_id);

COMMIT;
