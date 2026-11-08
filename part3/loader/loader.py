import csv
import os
import time
from pathlib import Path

import psycopg2
from psycopg2 import sql

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "csvdb")
DB_USER = os.getenv("DB_USER", "lab")
DB_PASSWORD = os.getenv("DB_PASSWORD", "lab")
DATA_DIR = os.getenv("DATA_DIR", "/data")


def detect_delimiter(header_line):
    counts = {d: header_line.count(d) for d in ",;\t"}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else ","


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        delimiter = detect_delimiter(f.readline())
        f.seek(0)
        all_rows = [row for row in csv.reader(f, delimiter=delimiter) if row]

    if not all_rows:
        return [], []

    header = [name.strip() for name in all_rows[0]]
    header = [name if name else f"column_{i + 1}" for i, name in enumerate(header)]
    return header, all_rows[1:]


def connect_with_retry(attempts=10):
    for attempt in range(1, attempts + 1):
        try:
            return psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
        except psycopg2.OperationalError:
            print(f"Database is not ready, attempt {attempt}/{attempts}...")
            time.sleep(2)
    raise RuntimeError("Could not connect to the database")


def load_file(conn, path):
    header, rows = read_csv(path)
    if not header:
        print(f"{path.name}: empty file, skipped")
        return

    table = path.stem.lower()
    n = len(header)

    with conn.cursor() as cur:
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table)))
        columns = sql.SQL(", ").join(
            sql.SQL("{} TEXT").format(sql.Identifier(name)) for name in header
        )
        cur.execute(sql.SQL("CREATE TABLE {} ({})").format(sql.Identifier(table), columns))

        insert = sql.SQL("INSERT INTO {} VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(", ").join(sql.Placeholder() * n),
        )
        data = [(row + [""] * n)[:n] for row in rows]
        cur.executemany(insert, data)

    conn.commit()
    print(f"{path.name}: loaded {len(rows)} rows, {n} columns -> table '{table}'")


def main():
    files = sorted(Path(DATA_DIR).glob("*.csv"))
    if not files:
        print(f"No CSV files found in {DATA_DIR}")
        return

    print(f"Found {len(files)} CSV file(s) in {DATA_DIR}")
    conn = connect_with_retry()
    try:
        for path in files:
            load_file(conn, path)
    finally:
        conn.close()
    print("Done")


if __name__ == "__main__":
    main()