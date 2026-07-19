-- V021__exams.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.exams (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  title text NOT NULL,
  description text,
  duration interval,
  passing_score numeric(5,2),
  max_attempts int DEFAULT 1,
  available_from timestamptz,
  available_until timestamptz,
  random_questions boolean DEFAULT false,
  show_results boolean DEFAULT true,
  status text NOT NULL DEFAULT 'draft',
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
