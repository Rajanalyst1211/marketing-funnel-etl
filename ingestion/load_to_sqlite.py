import sqlite3
import pandas as pd
import os

RAW_DIR = "data/raw"
DB_PATH = "data/marketing_funnel.db"

def load_csv_to_sqlite(conn, csv_path, table_name):
    """
    Reads a CSV file and loads it into a SQLite table.
    if_exists='replace' means it overwrites the table on each run —
    safe for raw layer since we always reload from source.
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"  Loaded {len(df):,} rows into table: {table_name}")

def validate_load(conn):
    """
    Run basic checks after loading to confirm
    data landed correctly in SQLite.
    """
    print("\nValidation checks:")

    cursor = conn.cursor()

    tables = ["raw_leads", "raw_campaign_spend"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,} rows")

    # Check for nulls in critical columns
    cursor.execute("SELECT COUNT(*) FROM raw_leads WHERE lead_id IS NULL")
    null_ids = cursor.fetchone()[0]
    print(f"  Null lead_ids: {null_ids} (expected: 0)")

    # Show date range of the data
    cursor.execute("SELECT MIN(created_date), MAX(created_date) FROM raw_leads")
    min_date, max_date = cursor.fetchone()
    print(f"  Date range: {min_date} to {max_date}")

def main():
    print(f"Connecting to SQLite database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    print("\nLoading raw data...")
    load_csv_to_sqlite(conn, f"{RAW_DIR}/leads.csv",          "raw_leads")
    load_csv_to_sqlite(conn, f"{RAW_DIR}/campaign_spend.csv", "raw_campaign_spend")

    validate_load(conn)

    conn.close()
    print(f"\nDone! Database saved at: {DB_PATH}")
    print("Open it with the SQLite Viewer extension in VS Code.")

if __name__ == "__main__":
    main()

