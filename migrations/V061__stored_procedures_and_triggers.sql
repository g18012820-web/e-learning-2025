-- V061__stored_procedures_and_triggers.sql
BEGIN;

-- Stored procedure: purchase_course
-- This procedure performs the purchase transaction atomically:
-- 1) Check wallet balance
-- 2) Deduct amount from wallet
-- 3) Insert wallet_transaction
-- 4) Insert student_course
-- 5) Return success or raise exception

CREATE OR REPLACE FUNCTION public.purchase_course(p_user_id uuid, p_course_id uuid, p_amount numeric)
RETURNS TABLE(success boolean, message text) LANGUAGE plpgsql AS $$
DECLARE
  v_wallet_id uuid;
  v_balance numeric(14,2);
BEGIN
  -- lock wallet row
  SELECT id, balance INTO v_wallet_id, v_balance FROM public.wallets WHERE user_id = p_user_id FOR UPDATE;
  IF v_wallet_id IS NULL THEN
    RETURN QUERY SELECT false, 'Wallet not found';
    RETURN;
  END IF;
  IF v_balance < p_amount THEN
    RETURN QUERY SELECT false, 'Insufficient balance';
    RETURN;
  END IF;

  -- perform deductions
  UPDATE public.wallets SET balance = balance - p_amount, total_spent = total_spent + p_amount WHERE id = v_wallet_id;
  INSERT INTO public.wallet_transactions (wallet_id, transaction_type, amount, description, status) VALUES (v_wallet_id, 'Purchase', p_amount, concat('Purchase course ', p_course_id::text), 'completed');
  INSERT INTO public.student_courses (user_id, course_id, purchase_type, purchased_at, progress, completed) VALUES (p_user_id, p_course_id, 'wallet', now(), 0, false) ON CONFLICT DO NOTHING;

  RETURN QUERY SELECT true, 'Purchase completed';
END;
$$;

-- Stored procedure: use_activation_code
CREATE OR REPLACE FUNCTION public.use_activation_code(p_user_id uuid, p_code text)
RETURNS TABLE(success boolean, message text) LANGUAGE plpgsql AS $$
DECLARE
  v_code_id uuid;
  v_usage_limit int;
  v_usage_count int;
  v_expires timestamptz;
BEGIN
  SELECT id, usage_limit, usage_count, expires_at INTO v_code_id, v_usage_limit, v_usage_count, v_expires FROM public.activation_codes WHERE code = p_code FOR UPDATE;
  IF v_code_id IS NULL THEN
    RETURN QUERY SELECT false, 'Code not found';
    RETURN;
  END IF;
  IF v_expires IS NOT NULL AND v_expires < now() THEN
    RETURN QUERY SELECT false, 'Code expired';
    RETURN;
  END IF;
  IF v_usage_limit IS NOT NULL AND v_usage_count >= v_usage_limit THEN
    RETURN QUERY SELECT false, 'Usage limit exceeded';
    RETURN;
  END IF;

  -- apply code (example: account activation)
  UPDATE public.activation_codes SET usage_count = usage_count + 1 WHERE id = v_code_id;
  INSERT INTO public.code_usage (code_id, user_id, used_at) VALUES (v_code_id, p_user_id, now());
  UPDATE public.users SET activation_completed = true, status = 'active' WHERE id = p_user_id;

  RETURN QUERY SELECT true, 'Code applied successfully';
END;
$$;

COMMIT;
