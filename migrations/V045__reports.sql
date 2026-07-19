-- V045__reports.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text,
  params jsonb,
  schedule text,
  last_run timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
