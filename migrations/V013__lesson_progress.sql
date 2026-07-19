-- V013__lesson_progress.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.lesson_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  lesson_id uuid REFERENCES public.lessons(id) ON DELETE CASCADE,
  watch_time bigint DEFAULT 0,
  completion_percentage numeric(5,2) DEFAULT 0,
  completed boolean DEFAULT false,
  last_position bigint DEFAULT 0,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_progress_user_lesson ON public.lesson_progress (user_id, lesson_id);
CREATE INDEX IF NOT EXISTS ix_progress_user ON public.lesson_progress (user_id);
CREATE TRIGGER IF NOT EXISTS trg_lesson_progress_set_updated_at BEFORE UPDATE ON public.lesson_progress
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
