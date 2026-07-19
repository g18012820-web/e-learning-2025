-- V020__code_usage.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.code_usage (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code_id uuid REFERENCES public.activation_codes(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.users(id),
  used_at timestamptz NOT NULL DEFAULT now(),
  ip_address inet,
  device jsonb
);

CREATE INDEX IF NOT EXISTS ix_code_usages_code ON public.code_usage (code_id);

COMMIT;
