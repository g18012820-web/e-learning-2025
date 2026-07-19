-- V009__lesson_attachments.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.lesson_attachments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid REFERENCES public.lessons(id) ON DELETE CASCADE,
  file_name text NOT NULL,
  file_type text,
  file_size bigint,
  file_url text NOT NULL,
  download_allowed boolean DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_attachments_lesson ON public.lesson_attachments (lesson_id);

COMMIT;
