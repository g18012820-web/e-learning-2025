-- V002__users.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name text NOT NULL,
  last_name text NOT NULL,
  email citext NOT NULL,
  phone text,
  wilaya text,
  password_hash text NOT NULL,
  avatar text,
  role text NOT NULL CHECK (role IN ('owner','student')),
  status text NOT NULL CHECK (status IN ('active','pending_activation','suspended','banned','deleted')),
  activation_required boolean NOT NULL DEFAULT false,
  activation_completed boolean NOT NULL DEFAULT false,
  last_login timestamptz,
  last_ip inet,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz,
  is_migrated boolean NOT NULL DEFAULT false
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_users_email_active ON public.users (email) WHERE deleted_at IS NULL;
CREATE UNIQUE INDEX IF NOT EXISTS ux_users_phone_active ON public.users (phone) WHERE phone IS NOT NULL AND deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS ix_users_role_status ON public.users (role, status);
CREATE INDEX IF NOT EXISTS ix_users_created_at ON public.users (created_at);

CREATE TRIGGER IF NOT EXISTS trg_users_set_updated_at BEFORE UPDATE ON public.users
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

COMMIT;
