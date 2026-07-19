-- V017__wallet_transactions.sql
BEGIN;

-- Partitioned table by range on created_at for scalability
CREATE TABLE IF NOT EXISTS public.wallet_transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  wallet_id uuid REFERENCES public.wallets(id) ON DELETE CASCADE,
  transaction_type text NOT NULL,
  amount numeric(14,2) NOT NULL,
  description text,
  reference text,
  status text NOT NULL DEFAULT 'completed',
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- Create initial partition for current year
CREATE TABLE IF NOT EXISTS public.wallet_transactions_2026 PARTITION OF public.wallet_transactions
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX IF NOT EXISTS ix_wallet_transactions_wallet ON public.wallet_transactions (wallet_id);

COMMIT;
