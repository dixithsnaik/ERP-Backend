from flask import Flask
import controllers.users
from dataModels.datbaseSetup import init_db
import logging
from controllers import greet, users, PurchaseOrdersIn


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

#greeting routes
app.add_url_rule('/hello', 'hello', greet.hello)
app.add_url_rule('/users', 'users', users.getUsers)

# PO routes
app.add_url_rule('/pendingpos', 'pendingpos', controllers.PurchaseOrdersIn.getPendingPOs, methods=['GET'])


if __name__ == '__main__':
    try:
        # Initialize the database
        logging.info("Initializing database...")
        res = init_db()
        if res:
            print("Database initialized successfully.")
        else:
            print("Database initialization failed.")
            logging.error("Database initialization failed.")
            exit(1)
        logging.info("Database initialized successfully.")
        
        app.run(debug=True, host='0.0.0.0', port=5000) 
    except Exception as e:
        logging.error(f"An error occurred during startup: {e}")
