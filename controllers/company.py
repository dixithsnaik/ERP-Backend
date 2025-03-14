from flask import request, jsonify
import logging

# internal imports
from dataControllers.company import getCompanyDetailsDB, updateCompanyDetailsDB
# from dataControllers.Customers import getCustomerName


def getCompanyDetails():
    """
    Controller function to fetch company details from the database.
    """
    try:
        companyDetails = getCompanyDetailsDB()
        return jsonify(companyDetails), 200

    except Exception as e:
        logging.error(f"Error fetching company details: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    

def updateCompanyDetails():
    """
    Controller function to update company details in the database.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = updateCompanyDetailsDB(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error updating company details: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500