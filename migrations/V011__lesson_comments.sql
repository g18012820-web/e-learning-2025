-- V011__lesson_comments.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.lesson_comments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid REFERENCES public.lessons(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.users(id) ON DELETE SET NULL,
  parent_id uuid REFERENCES public.lesson_comments(id) ON DELETE CASCADE,
  body text NOT NULL,
  status text NOT NULL DEFAULT 'visible',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz
);

CREATE INDEX IF NOT EXISTS ix_lesson_comments_lesson ON public.lesson_comments (lesson_id);
CREATE TRIGGER IF NOT EXISTS trg_lesson_comments_set_updated_at BEFORE UPDATE ON public.lesson_comments
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
