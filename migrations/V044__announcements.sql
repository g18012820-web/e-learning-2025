-- V044__announcements.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.announcements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text,
  body text,
  start_at timestamptz,
  end_at timestamptz,
  status text DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
