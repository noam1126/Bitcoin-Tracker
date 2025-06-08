CREATE TABLE IF NOT EXISTS bitcoin_stats (
    id SERIAL PRIMARY KEY,
    price NUMERIC,
    min NUMERIC,
    max NUMERIC,
    avg NUMERIC,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
