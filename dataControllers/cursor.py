"""
This file will be used to control the cursor of the sql database.
"""
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Credentials (Use environment variables)
DB_NAME = os.getenv("DB_NAME", "ERPDB")
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "root")
HOST = os.getenv("DB_HOST", "localhost")

cursor = None
connection = None

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DB_NAME
)

connection.autocommit = True

cursor = connection.cursor(dictionary=True)