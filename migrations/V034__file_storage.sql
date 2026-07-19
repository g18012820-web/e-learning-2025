-- V034__file_storage.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.file_storage (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  media_id uuid REFERENCES public.media_library(id) ON DELETE CASCADE,
  path text,
  size bigint,
  content_type text,
  storage_provider text,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
