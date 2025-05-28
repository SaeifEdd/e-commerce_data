import sqlite3
import pandas as pd


def load(csv_path: str, db_path: str):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("smartphones", conn, if_exists="replace", index=False)
    conn.close()
