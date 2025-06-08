import os
import time
import requests
import psycopg2

values = []

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        price = response.json()["bitcoin"]["usd"]
        return float(price)
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

def calculate_stats(values):
    avg = sum(values) / len(values)
    return min(values), max(values), avg

def get_recommendation(current_price, avg_price):
    if current_price < avg_price:
        return "BUY"
    elif current_price > avg_price:
        return "SELL"
    else:
        return "HOLD"

def write_to_db(conn, price, min_v, max_v, avg_v, recommendation):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bitcoin_stats (price, min, max, avg, recommendation)
            VALUES (%s, %s, %s, %s, %s)
        """, (price, min_v, max_v, avg_v, recommendation))
        conn.commit()

def connect_with_retry(max_retries=5, delay=5):
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                database=os.getenv("DB_NAME", "btcdb"),
                user=os.getenv("DB_USER", "btcuser"),
                password=os.getenv("DB_PASSWORD", "btcpass")
            )
            print("Connected to DB")
            return conn
        except psycopg2.OperationalError as e:
            print(f"DB connection attempt {i+1} failed: {e}")
            time.sleep(delay)
    print("Failed to connect to DB after retries, exiting...")
    exit(1)

def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bitcoin_stats (
                id SERIAL PRIMARY KEY,
                price NUMERIC,
                min NUMERIC,
                max NUMERIC,
                avg NUMERIC,
                recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def main():
    conn = connect_with_retry()
    create_table_if_not_exists(conn)
    while True:
        price = get_bitcoin_price()
        if price is None:
            print("Skipping this round due to fetch error.")
            time.sleep(60)
            continue

        values.append(price)
        min_v, max_v, avg_v = calculate_stats(values)
        recommendation = get_recommendation(price, avg_v)

        print(f"💰 Current: {price:.2f} | Min: {min_v:.2f} | Max: {max_v:.2f} | Avg: {avg_v:.2f} → {recommendation}")

        write_to_db(conn, price, min_v, max_v, avg_v, recommendation)
        time.sleep(60)

if __name__ == "__main__":
    main()
