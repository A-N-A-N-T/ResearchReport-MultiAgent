import sqlite3
import os

DB_PATH = "database/research_history.db"

#DATABASE CONNECTION FUNCTION
def get_connection():
    return sqlite3.connect(DB_PATH)


#Schema creation function
def create_table():

    conn = get_connection()
    curser = conn.cursor()

    curser.execute(
        """
         CREATE TABLE IF NOT EXISTS research_history(
          id TEXT PRIMARY KEY,
          topic TEXT NOT NULL,
          report TEXT NOT NULL,
          feedback TEXT NOT NULL,
          search_results TEXT,
          pdf_path TEXT,
          created_at TIMESTAMP CURRENT_TIMESTAMP
         )
        """
    )

    conn.commit()
    conn.close()

