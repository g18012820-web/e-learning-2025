-- V049__security_settings.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.security_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  key text NOT NULL UNIQUE,
  value jsonb,
  updated_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
