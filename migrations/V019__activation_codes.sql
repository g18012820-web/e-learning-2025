-- V019__activation_codes.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.activation_codes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code text NOT NULL UNIQUE,
  code_type text NOT NULL,
  value numeric(14,2),
  usage_limit int DEFAULT 1,
  usage_count int DEFAULT 0,
  expires_at timestamptz,
  status text NOT NULL DEFAULT 'active',
  created_by uuid REFERENCES public.users(id),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_activation_codes_status ON public.activation_codes (status);

COMMIT;
