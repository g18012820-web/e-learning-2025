-- V054__rate_limits.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.rate_limits (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject text NOT NULL,
  limit_per_minute int,
  window_seconds int,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
