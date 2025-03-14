from flask import request, jsonify
import logging

# internal imports
from dataControllers.Quotations import getUnapprovedQuotationsDB
from dataControllers.Customers import getCustomerName

def getUnapprovedQuotations():
    """
    This function fetches all the unapproved quotations from the database and returns them as a JSON object.
    {
    "quotationid": "INT",
    "customer_name": "INT", //getfrom customet table
    "rfqid": "INT",
    "name": "VARCHAR(255)",
    "deliveryDate": "DATE",
    "createdBy":"string", // get from users(userid) -> username
    "AdminApproved": "BOOLEAN",
    }
    """

    try:
        # first fetch the unapproved quotations from the database
        unapprovedQuotations = getUnapprovedQuotationsDB()

        print(unapprovedQuotations)

        # now fetch the name of the customers from the database and update the unapprovedQuotations
        for quotation in unapprovedQuotations:
            customerName = getCustomerName(quotation["customerid"])
            print(f"customerName: {customerName}")
            quotation["customer_name"] = customerName

        return jsonify({"unapprovedQuotations": unapprovedQuotations})

    except Exception as e:
        # logging.error(f"An error occurred while fetching unapproved quotations: {e}")
        return jsonify({"error": str(e)})



