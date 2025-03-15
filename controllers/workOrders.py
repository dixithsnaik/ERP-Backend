from flask import request, jsonify
import logging

# internal imports
from dataControllers.workOrders import fetchAllWorkOrdersDB
def fetchAllWorkOrders():
    """
    Controller function to fetch all work orders from the database.
    """
    try:
        allWorkOrders = fetchAllWorkOrdersDB()
        return jsonify(allWorkOrders), 200

    except Exception as e:
        logging.error(f"Error fetching work orders: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500