-- V039__banners.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.banners (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text,
  image text,
  url text,
  position int DEFAULT 0,
  status text DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
