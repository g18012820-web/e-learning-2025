-- V022__questions.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  exam_id uuid REFERENCES public.exams(id) ON DELETE CASCADE,
  type text NOT NULL,
  question text NOT NULL,
  explanation text,
  score numeric(6,2) DEFAULT 1,
  order_number int DEFAULT 0,
  options jsonb
);

CREATE INDEX IF NOT EXISTS ix_questions_exam ON public.questions (exam_id);

COMMIT;
