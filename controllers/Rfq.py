from flask import request, jsonify
import logging

# internal imports
from dataControllers.Rfq import postRfqDetailsDB, fetchAllRfqDetailsDB
from Utils.Customers import getCustomerName

def createRfq():
    """
    Controller function to post RFQ (Request for Quotation) data into the database.
    """
    try:
        data = request.get_json()
        # print(data)

        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = postRfqDetailsDB(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error creating RFQ: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
def fetchAllRfqs():
    """
    Controller function to fetch all RFQs from the database and then also fetchihg the customer name from the customer id received from rfq table.
    """
    try:
        allRfqDetails = fetchAllRfqDetailsDB()

        for rfqDetail in allRfqDetails:
            customerName = getCustomerName(rfqDetail["customerid"])
            rfqDetail["customer_name"] = customerName


        return jsonify(allRfqDetails), 200

    except Exception as e:
        logging.error(f"Error fetching RFQs: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def getPendingRfqs():
    try:
        pendingRfqs = fetchAllRfqDetailsDB()

        for rfqDetail in pendingRfqs:
            customerName = getCustomerName(rfqDetail["customerid"])
            rfqDetail["customer_name"] = customerName

        return jsonify(pendingRfqs), 200
    
    except Exception as e:
        logging.error(f"Error fetching pending RFQs: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500