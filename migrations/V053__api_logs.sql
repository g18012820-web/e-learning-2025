-- V053__api_logs.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.api_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  api_key_id uuid REFERENCES public.api_keys(id),
  path text,
  method text,
  status int,
  latency_ms int,
  request_headers jsonb,
  request_body jsonb,
  response_body jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS public.api_logs_2026 PARTITION OF public.api_logs
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

COMMIT;
