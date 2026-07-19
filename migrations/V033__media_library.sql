-- V033__media_library.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.media_library (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id uuid REFERENCES public.users(id),
  type text,
  provider text,
  original_url text,
  secure_url text,
  metadata jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_media_library_owner ON public.media_library (owner_id);

COMMIT;
