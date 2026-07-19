-- V038__search_history.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.search_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id),
  query text,
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS public.search_history_2026 PARTITION OF public.search_history
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

COMMIT;
