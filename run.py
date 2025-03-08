from flask import Flask
from dataModels.datbaseSetup import init_db , drop_tables
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask Server is Running & Database is Ready!"

if __name__ == '__main__':
    try:
        # Initialize the database
        logging.info("Initializing database...")
        init_db()
        logging.info("Database initialized successfully.")
        
        app.run(debug=True, host='0.0.0.0', port=5000) 
    except Exception as e:
        logging.error(f"An error occurred during startup: {e}")
