-- Migration: Add email_verified and otp_attempts columns
-- Date: 2026-02-22

-- Add email_verified column
ALTER TABLE accounts ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

-- Add otp_attempts column
ALTER TABLE accounts ADD COLUMN otp_attempts INT DEFAULT 0;
