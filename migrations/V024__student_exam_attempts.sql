-- V024__student_exam_attempts.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.student_exam_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  exam_id uuid REFERENCES public.exams(id) ON DELETE CASCADE,
  started_at timestamptz NOT NULL DEFAULT now(),
  finished_at timestamptz,
  score numeric(6,2),
  passed boolean,
  attempt_number int DEFAULT 1
);

CREATE INDEX IF NOT EXISTS ix_student_exams_user ON public.student_exam_attempts (user_id);

COMMIT;
