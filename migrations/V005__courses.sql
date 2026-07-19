-- V005__courses.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.courses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id uuid REFERENCES public.subjects(id) ON DELETE SET NULL,
  teacher_id uuid REFERENCES public.teachers(id) ON DELETE SET NULL,
  title text NOT NULL,
  description text,
  cover text,
  banner text,
  price numeric(12,2) NOT NULL DEFAULT 0,
  currency varchar(3) NOT NULL DEFAULT 'DZD',
  sale_price numeric(12,2),
  level text,
  duration interval,
  lessons_count int DEFAULT 0,
  status text NOT NULL DEFAULT 'draft',
  allow_purchase boolean NOT NULL DEFAULT true,
  featured boolean NOT NULL DEFAULT false,
  published_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_courses_subject ON public.courses (subject_id);
CREATE INDEX IF NOT EXISTS ix_courses_teacher ON public.courses (teacher_id);
CREATE INDEX IF NOT EXISTS ix_courses_status_featured ON public.courses (status, featured);
CREATE TRIGGER IF NOT EXISTS trg_courses_set_updated_at BEFORE UPDATE ON public.courses
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
