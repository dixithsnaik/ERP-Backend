# flask and other python imports
from flask import request, jsonify
import logging

# internal imports
from dataControllers.PurchaseOrdersIn import getPendingPOs
from Utils.Customers import getCustomerName


def getPendingPOs():

    """
    This function fetches all the pending POs from the database and returns them as a JSON object.
    res=[{ //table name purchase_order
        "workordernumber": "",
        "po_number": "",
        "customerName": "", //using customerid from customer table
        "po_date": "",
        "amount": "",
        "project_engineers":"",
        "quality_engineers":"",
        "delivery_date": "", //sort by this
        "status": "", // fetch those are 'Pending' among ('Pending', 'Delivered', 'Shipped', 'Cancelled')
        "remarks": "",
        },
        ]
    """

    # userID = request.args.get("userID")

    try:
        # first fetch the pending POs from the database
        pendingPOs = getPendingPOs()

        # now fetch the name of the customers from the database and update the pendingPOs
        pendingPOs.map(lambda po: po.update({"customerName": getCustomerName(po["customerid"])}))

        return jsonify({"pendingPOs": pendingPOs})

    except Exception as e:
        logging.error(f"An error occurred while fetching pending POs: {e}")
        return jsonify({"error": str(e)})