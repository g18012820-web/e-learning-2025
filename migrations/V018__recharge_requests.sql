-- V018__recharge_requests.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.recharge_requests (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  payment_method text NOT NULL,
  amount numeric(14,2) NOT NULL,
  payment_image text,
  transaction_number text,
  notes text,
  status text NOT NULL DEFAULT 'pending',
  reviewed_by uuid REFERENCES public.users(id),
  reviewed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_recharge_requests_user ON public.recharge_requests (user_id);

COMMIT;
