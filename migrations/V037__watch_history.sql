-- V037__watch_history.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.watch_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  lesson_id uuid REFERENCES public.lessons(id) ON DELETE CASCADE,
  watched_at timestamptz NOT NULL DEFAULT now(),
  position bigint DEFAULT 0
) PARTITION BY RANGE (watched_at);

CREATE TABLE IF NOT EXISTS public.watch_history_2026 PARTITION OF public.watch_history
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_watch_history_user ON public.watch_history (user_id);

COMMIT;
