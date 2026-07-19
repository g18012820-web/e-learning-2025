-- V046__statistics_cache.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.statistics_cache (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  key text NOT NULL UNIQUE,
  value jsonb,
  refreshed_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
