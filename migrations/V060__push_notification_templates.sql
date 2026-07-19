-- V060__push_notification_templates.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.push_notification_templates (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL UNIQUE,
  title text,
  body text,
  data jsonb,
  lang text DEFAULT 'ar',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER IF NOT EXISTS trg_push_templates_set_updated_at BEFORE UPDATE ON public.push_notification_templates
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
