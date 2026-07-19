-- V029__devices.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.devices (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  device_fingerprint text NOT NULL,
  device_name text,
  last_seen timestamptz,
  ip_address inet,
  app_version text,
  created_at timestamptz NOT NULL DEFAULT now(),
  revoked boolean DEFAULT false
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_devices_fingerprint_user ON public.devices (user_id, device_fingerprint);

COMMIT;
