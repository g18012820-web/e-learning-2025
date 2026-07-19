-- V050__backup_jobs.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.backup_jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_type text NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  scheduled_at timestamptz,
  finished_at timestamptz,
  meta jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
