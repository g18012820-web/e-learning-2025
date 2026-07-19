-- V057__maintenance_mode.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.maintenance_mode (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  enabled boolean DEFAULT false,
  message text,
  started_at timestamptz,
  ended_at timestamptz,
  updated_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
