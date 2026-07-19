-- V047__system_settings.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.system_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  key text NOT NULL UNIQUE,
  value jsonb,
  description text,
  updated_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
