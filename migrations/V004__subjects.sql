-- V004__subjects.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.subjects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text,
  icon text,
  image text,
  color varchar(7),
  display_order int DEFAULT 0,
  status text NOT NULL DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_subjects_display_order ON public.subjects (display_order);
CREATE TRIGGER IF NOT EXISTS trg_subjects_set_updated_at BEFORE UPDATE ON public.subjects
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
