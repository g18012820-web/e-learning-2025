-- V025__student_answers.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.student_answers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  attempt_id uuid REFERENCES public.student_exam_attempts(id) ON DELETE CASCADE,
  question_id uuid REFERENCES public.questions(id) ON DELETE CASCADE,
  answer jsonb,
  is_correct boolean
);

COMMIT;
