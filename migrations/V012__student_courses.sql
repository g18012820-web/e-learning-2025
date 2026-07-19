-- V012__student_courses.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.student_courses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  purchase_type text,
  purchased_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz,
  progress numeric(5,2) DEFAULT 0,
  completed boolean DEFAULT false
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_student_course_user_course ON public.student_courses (user_id, course_id);
CREATE INDEX IF NOT EXISTS ix_student_courses_user ON public.student_courses (user_id);

COMMIT;
