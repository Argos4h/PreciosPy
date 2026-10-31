import sqlite3

for db_path in ['dist/catalog_latest.db', 'mobile/assets/db/catalog_latest.db']:
    print(f"--- DB: {db_path} ---")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    for row in c.fetchall():
        print(f"Table: {row[0]}")
        print(row[1])

