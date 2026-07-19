-- V003__teachers.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.teachers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name text NOT NULL,
  avatar text,
  biography text,
  specialization text,
  experience_years int,
  certificates jsonb,
  social_links jsonb,
  email citext,
  phone text,
  status text NOT NULL DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_teachers_specialization ON public.teachers USING gin (to_tsvector('simple', coalesce(specialization,'')));
CREATE TRIGGER IF NOT EXISTS trg_teachers_set_updated_at BEFORE UPDATE ON public.teachers
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
