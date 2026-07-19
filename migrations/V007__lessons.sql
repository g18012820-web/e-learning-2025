-- V007__lessons.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.lessons (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  section_id uuid REFERENCES public.course_sections(id) ON DELETE SET NULL,
  title text NOT NULL,
  description text,
  lesson_type text NOT NULL DEFAULT 'video',
  content jsonb,
  order_number int DEFAULT 0,
  duration interval,
  release_date timestamptz,
  live_date timestamptz,
  is_locked boolean DEFAULT false,
  is_hidden boolean DEFAULT false,
  status text NOT NULL DEFAULT 'draft',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_lessons_course_order ON public.lessons (course_id, order_number);
CREATE TRIGGER IF NOT EXISTS trg_lessons_set_updated_at BEFORE UPDATE ON public.lessons
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
