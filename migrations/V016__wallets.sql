-- V016__wallets.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.wallets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE UNIQUE,
  balance numeric(14,2) DEFAULT 0,
  total_recharged numeric(14,2) DEFAULT 0,
  total_spent numeric(14,2) DEFAULT 0,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TRIGGER IF NOT EXISTS trg_wallets_set_updated_at BEFORE UPDATE ON public.wallets
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
