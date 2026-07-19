-- V048__payment_settings.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.payment_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  provider text,
  credentials jsonb,
  enabled boolean DEFAULT false,
  updated_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
