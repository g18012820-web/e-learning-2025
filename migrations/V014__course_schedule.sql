-- V014__course_schedule.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.course_schedule (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  start_date timestamptz,
  end_date timestamptz,
  timezone text,
  notes text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_course_schedule_course ON public.course_schedule (course_id);

COMMIT;
