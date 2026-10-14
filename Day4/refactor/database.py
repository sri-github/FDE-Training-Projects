import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

# Homework-specific database name (diabetes_queue_db) with classroom credentials
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://fde_user:FDE_Local_2026@localhost:5432/diabetes_queue_db"
)

def get_connection():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn