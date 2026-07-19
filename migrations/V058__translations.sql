-- V058__translations.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.translations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  namespace text NOT NULL,
  key text NOT NULL,
  locale text NOT NULL,
  value text,
  last_updated timestamptz NOT NULL DEFAULT now(),
  UNIQUE(namespace,key,locale)
);

COMMIT;
