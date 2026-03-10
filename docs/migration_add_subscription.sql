-- ========================================================
-- THÊM CỘT SUBSCRIPTION VÀO BẢNG ACCOUNTS
-- ========================================================
-- Chạy file này trong MySQL để thêm các cột subscription

ALTER TABLE accounts
ADD COLUMN subscription_type ENUM('free', 'plus', 'pro', 'vip', 'max') DEFAULT 'free',
ADD COLUMN subscription_start TIMESTAMP NULL,
ADD COLUMN subscription_end TIMESTAMP NULL,
ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- ========================================================
-- GÓI SUBSCRIPTION
-- ========================================================
-- plus: 1 tháng
-- pro: 3 tháng
-- vip: 6 tháng
-- max: 12 tháng
