import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os
# Remove this line if present because 'userdata' is not available outside Colab
# from google.colab import userdata

# Use os.getenv() instead of os.get()
RENDER_DB_HOST = os.getenv("RENDER_DB_HOST")
RENDER_DB_NAME = os.getenv("RENDER_DB_NAME")
RENDER_DB_PASSWORD = os.getenv("RENDER_DB_PASSWORD")
RENDER_DB_PORT = os.getenv("RENDER_DB_PORT")
RENDER_DB_USER = os.getenv("RENDER_DB_USER")
# Render PostgreSQL connection details
DB_CONFIG = {
    'host': 'dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com',      # e.g., 'dpg-cn5v9u8l6cac73bs9ug0-a'
    'database': 'sugeetha',   # e.g., 'mydb'
    'user': 'sugeetha_user',            # e.g., 'mydb_user'
    'password': '1sZvre5q7iok697JpIre1qCJiu5qJ9AV',    # Find in Render dashboard
    'port': 5432                     # Usually 5432
}

def test_psycopg2_connection():
    try:

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        print("✔ PostgreSQL Render connection successful!")
        print("Server version:", cursor.fetchone()[0])
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

test_psycopg2_connection()


