-- V015__live_sessions.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.live_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid REFERENCES public.courses(id) ON DELETE CASCADE,
  lesson_id uuid REFERENCES public.lessons(id) ON DELETE CASCADE,
  title text,
  description text,
  start_at timestamptz,
  end_at timestamptz,
  provider text,
  meeting_url text,
  host_user_id uuid REFERENCES public.users(id),
  status text NOT NULL DEFAULT 'scheduled',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_live_sessions_course ON public.live_sessions (course_id);

COMMIT;
