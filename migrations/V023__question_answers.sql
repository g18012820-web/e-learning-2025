-- V023__question_answers.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.question_answers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id uuid REFERENCES public.questions(id) ON DELETE CASCADE,
  answer jsonb,
  is_correct boolean DEFAULT false
);

COMMIT;
