-- seed/seed_initial.sql
BEGIN;

-- Create default owner user (password_hash placeholder: replace with bcrypt hash)
INSERT INTO public.users (id, first_name, last_name, email, password_hash, role, status, activation_required, activation_completed, created_at, is_migrated)
VALUES (gen_random_uuid(), 'Platform', 'Owner', 'owner@example.com', 'REPLACE_WITH_HASH', 'owner', 'active', false, true, now(), true)
RETURNING id;

-- Insert default system settings
INSERT INTO public.system_settings (id, key, value, description) VALUES (gen_random_uuid(), 'platform_name', jsonb_build_object('value','Elera'), 'Platform name');
INSERT INTO public.system_settings (id, key, value, description) VALUES (gen_random_uuid(), 'enable_account_activation', jsonb_build_object('value', true), 'Require activation for new accounts');
INSERT INTO public.system_settings (id, key, value, description) VALUES (gen_random_uuid(), 'allow_multiple_sessions', jsonb_build_object('value', false), 'Allow multiple simultaneous sessions per user');

COMMIT;
