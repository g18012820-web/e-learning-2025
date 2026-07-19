-- V052__api_keys.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.api_keys (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  key text NOT NULL UNIQUE,
  permissions jsonb,
  revoked boolean DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
