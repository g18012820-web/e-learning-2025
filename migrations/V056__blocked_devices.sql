-- V056__blocked_devices.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.blocked_devices (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  device_fingerprint text NOT NULL UNIQUE,
  reason text,
  expires_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
