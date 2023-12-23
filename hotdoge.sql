drop database hotdoge;

-- hotdogeデータベースを作成するクエリ
CREATE DATABASE IF NOT EXISTS hotdoge;
USE hotdoge;

-- ログイン情報を格納するテーブル
CREATE TABLE IF NOT EXISTS login_info (
    personal_id BIGINT PRIMARY KEY,
    referee_id BIGINT,
    login_date DATE,
    expiry_date DATE,
    whitelist ENUM('Yes', 'No')
);

-- 個人プロフィール情報を格納するテーブル
CREATE TABLE IF NOT EXISTS personal_key (
    personal_id BIGINT,
    private_key VARCHAR(255) PRIMARY KEY
);
