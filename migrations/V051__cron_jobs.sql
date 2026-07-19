-- V051__cron_jobs.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.cron_jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  schedule text,
  last_run timestamptz,
  status text DEFAULT 'idle',
  meta jsonb
);

COMMIT;
