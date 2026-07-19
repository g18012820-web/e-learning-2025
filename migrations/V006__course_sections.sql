-- V006__course_sections.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.course_sections (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  title text NOT NULL,
  description text,
  order_number int DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_course_sections_course_order ON public.course_sections (course_id, order_number);
CREATE TRIGGER IF NOT EXISTS trg_course_sections_set_updated_at BEFORE UPDATE ON public.course_sections
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
