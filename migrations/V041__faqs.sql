-- V041__faqs.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.faqs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question text NOT NULL,
  answer text,
  position int DEFAULT 0,
  status text DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
