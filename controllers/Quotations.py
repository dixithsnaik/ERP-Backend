from flask import request, jsonify
import logging

# internal imports
from dataControllers.Quotations import getUnapprovedQuotationsDB, getAllQuotationsDB, getPendingApprovalQuotationsDB, approvedQuotationDB
from dataControllers.Customers import getCustomerName

def approvedQuotation():
    """
    This function approves a quotation in the database.
    {
  "quotations": [
            {
            "quotationid": 502,
            "customerid": 102,
            "name": "Alice Smith",
            "emailAddress": "alice.smith@example.com",
            "phoneNumber": "9876543210",
            "deliveryDate": "2025-04-20",
            "AdminApproved": true,
            "itemDetails": {
                "items": [
                {
                    "itemDescription": "Voltage Regulator",
                    "partNumber": "VR-9012",
                    "quantity": 20,
                    "unitRateINR": 300,
                    "note": "For power supply circuits"
                }
                ],
                "notes": "Urgent delivery required."
            }
            }
        ]
        }

    """

    try:
        # approve the quotation in the database
        approvedQuotation = approvedQuotationDB()

        return jsonify({"approvedQuotation": approvedQuotation})

    except Exception as e:
        # logging.error(f"An error occurred while approving the quotation: {e}")
        return jsonify({"error": str(e)})

    

def getPendingApprovalQuotations():
    """
    This function fetches all the quotations pending approval from the database and returns them as a JSON object.
    {
        "quotationid": "INT",
        "customer_name": "STRING",//customer table
        "rfqid": "INT",
        "name": "VARCHAR(255)",
        "emailAddress": "VARCHAR(255)",
        "phoneNumber": "VARCHAR(15)",
        "termsAndConditions": "TEXT",
        "paymentTerms": "TEXT",
        "taxAndDuties": "TEXT",
        "briefDescription": "TEXT",
        "deliveryDate": "DATE",
        "packageAndForwarding": "TEXT",
        "createdBy": "INT",
        "AdminApproved": "BOOLEAN",
        "log": "JSON",
        "itemDetails": "JSON",
        "created_at": "TIMESTAMP",
        "updated_at": "TIMESTAMP"
    }
    """

    try:
        # fetch all quotations pending approval from the database
        pendingApprovalQuotations = getPendingApprovalQuotationsDB()

        for quotation in pendingApprovalQuotations:
            customerName = getCustomerName(quotation["customerid"])
            quotation["customer_name"] = customerName

        return jsonify({"pendingApprovalQuotations": pendingApprovalQuotations})

    except Exception as e:
        # logging.error(f"An error occurred while fetching pending approval quotations: {e}")
        return jsonify({"error": str(e)})



def getAllQuotations():
    """
    This function fetches all the quotations from the database and returns them as a JSON object.
    {
  "quotations": [
            {
            "quotationid": 501,
            "customerid": 101,
            "name": "John Doe",
            "emailAddress": "john.doe@example.com",
            "phoneNumber": "1234567890",
            "deliveryDate": "2025-04-15",
            "AdminApproved": null,
            "itemDetails": {
                "items": [
                {
                    "itemDescription": "Microcontroller Unit",
                    "partNumber": "MCU-1234",
                    "quantity": 10,
                    "unitRateINR": 1500,
                    "note": "High-performance MCU for industrial use"
                }
                ],
                "notes": "Bulk order, special discount applied."
            }
            }
        ]
        }
    """

    try:
        # fetch all quotations from the database
        allQuotations = getAllQuotationsDB()

        return jsonify({"quotations": allQuotations})

    except Exception as e:
        # logging.error(f"An error occurred while fetching all quotations: {e}")
        return jsonify({"error": str(e)})


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



