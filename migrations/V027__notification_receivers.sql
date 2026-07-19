-- V027__notification_receivers.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.notification_receivers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  notification_id uuid REFERENCES public.notifications(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  read_at timestamptz,
  delivered boolean DEFAULT false
);

CREATE INDEX IF NOT EXISTS ix_notification_receivers_user ON public.notification_receivers (user_id);

COMMIT;
