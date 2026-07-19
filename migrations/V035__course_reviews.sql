-- V035__course_reviews.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.course_reviews (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.users(id) ON DELETE SET NULL,
  rating int CHECK (rating >= 1 AND rating <= 5),
  title text,
  body text,
  approved boolean DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_course_reviews_course ON public.course_reviews (course_id);

COMMIT;
