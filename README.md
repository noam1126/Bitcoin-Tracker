Bitcoin Tracker

This project tracks Bitcoin prices, stores historical data in a PostgreSQL database, and provides simple analytics including min, max, average price, and a recommendation. It is built using Python and Docker.

Features

Retrieves the current Bitcoin price from an external API.

Stores price data in a PostgreSQL database.


Calculates and saves:

Minimum price

Maximum price

Average price

Simple recommendation (e.g. Buy / Sell)

Dockerized for easy deployment.


Technologies Used

Python

RestAPI

PostgreSQL

Docker & Docker Compose



Getting Started

1. Clone the repository

git clone https://github.com/noam1126/Bitcoin-Tracker.git

cd bitcoin-tracker


2. Build and Run the containers

docker-compose up --build


This will start both the API service and PostgreSQL database.

3. Initialize the Database


Ensure that the create_table.sql script is run inside the PostgreSQL container. You can do this manually:

docker exec -it bitcoin-tracker-db psql -U postgres -d postgres -f /init-db/create_table.sql

API / Script Behavior

The main.py script fetches Bitcoin price data, processes statistics, and inserts a row into the bitcoin_stats table.



The table schema includes:

CREATE TABLE IF NOT EXISTS bitcoin_stats (
    id SERIAL PRIMARY KEY,
    price NUMERIC,
    min NUMERIC,
    max NUMERIC,
    avg NUMERIC,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


File Structure

bitcoin-tracker/

├── app/
│   ├── main.py             # Python logic for fetching and storing price data

│   ├── Dockerfile          # App container definition

│   └── requirements.txt    # Python dependencies

├── init-db/
│   └── create_table.sql    # Table definition for PostgreSQL

├── docker-compose.yml      # Defines services (App + DB)



Troubleshooting

If data isn't appearing in the table:

Ensure the main.py script is running correctly.

Manually connect to DB container and query the table.

If created_at values are NULL:

Confirm that DEFAULT CURRENT_TIMESTAMP is set and no NULL is explicitly inserted.

Author

Noam Nachshon
noam1126@gmail.com
