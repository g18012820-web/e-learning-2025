-- V055__blocked_ips.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.blocked_ips (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ip inet NOT NULL UNIQUE,
  reason text,
  expires_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
