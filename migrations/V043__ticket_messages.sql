-- V043__ticket_messages.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.ticket_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id uuid REFERENCES public.support_tickets(id) ON DELETE CASCADE,
  user_id uuid REFERENCES public.users(id),
  body text NOT NULL,
  attachments jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
