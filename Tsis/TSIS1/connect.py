# connect.py
# ─────────────────────────────────────────────
# Returns a psycopg2 connection using config.py.
# ─────────────────────────────────────────────

import psycopg2
from config import DB_CONFIG


def get_connection():
    """Open and return a new database connection."""
    return psycopg2.connect(**DB_CONFIG)


def init_schema():
    """
    Run schema.sql and procedures.sql once to set up the database.
    Safe to call on every startup — uses IF NOT EXISTS / OR REPLACE.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                for sql_file in ("schema.sql", "procedures.sql"):
                    with open(sql_file, "r", encoding="utf-8") as f:
                        cur.execute(f.read())
        print("[DB] Schema initialised successfully.")
    finally:
        conn.close()