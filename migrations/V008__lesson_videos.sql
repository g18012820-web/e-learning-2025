-- V008__lesson_videos.sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.lesson_videos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lesson_id uuid REFERENCES public.lessons(id) ON DELETE CASCADE,
  provider text NOT NULL,
  original_url text,
  secure_url text,
  drm_type text,
  encryption_key text,
  quality text,
  subtitles jsonb,
  thumbnail text,
  duration interval,
  watermark_enabled boolean DEFAULT false,
  allow_download boolean DEFAULT false,
  allow_screenshot boolean DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_lesson_videos_lesson ON public.lesson_videos (lesson_id);

COMMIT;
