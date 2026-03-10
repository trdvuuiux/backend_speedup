-- Migration: Remove username column from accounts table
-- Date: 2026-02-22

-- Drop the username column if it exists
ALTER TABLE accounts DROP COLUMN IF EXISTS username;
