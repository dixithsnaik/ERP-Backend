# flask and other python imports
from flask import request, jsonify
import logging

# internal imports
from dataControllers.PurchaseOrdersIn import (  
                                                getPendingPOsDB,
                                                fetchPoDB,
                                                fetchProductionSlipDB,
                                                fetchWODB,
                                                createPODB,
                                                updatePODB
                                             )
from dataControllers.Customers import getCustomerName

def updatePO():
    """
    this function creates a new PO in the database.
    {
    "customerid": 1,
    "quotationid": 5,
    "employeeid": 10,
    "po_number": "PO-20240314-001",
    "po_date": "2025-03-14",
    "amount": 150000.50,
    "project_engineers": {"John Doe", "Jane Smith"},
    "quality_engineers": {"Robert Brown"},
    "delivery_date": "2025-04-01",
    "status": "Pending",
    "remarks": "Urgent delivery required",
    "contact_person_name": "Michael Johnson",
    "contact_person_email": "michael.johnson@example.com",
    "contact_person_phone": "+1-9876543210",
    "project_name": "Green Energy Project",
    "item_details": [
        {
            "item_id": 101,
            "description": "Solar Panels",
            "quantity": 50,
            "unit_price": 3000.00,
            "total_price": 150000.00
        }
    ],
    "work_order_issue_date": "2025-03-15",
    "instructions_for_delivery": "Deliver before noon",
    "critical_notes": "Handle with care",
    "logs": {}
    }
    """
    data = request.get_json()
    try:
        # first get the customer name
        customerName = getCustomerName(data["customerid"])

        data["customerName"] = customerName

        # then update the PO in the database
        updatePODB(data)

        return jsonify({"message": "PO updated successfully"})
    
    except Exception as e:
        logging.error(f"An error occurred while creating PO: {e}")
        return jsonify({"error": str(e)})


def createPO():
    """
    this function creates a new PO in the database.
    {
    "customerid": 1,
    "quotationid": 5,
    "employeeid": 10,
    "po_number": "PO-20240314-001",
    "po_date": "2025-03-14",
    "amount": 150000.50,
    "project_engineers": {"John Doe", "Jane Smith"},
    "quality_engineers": {"Robert Brown"},
    "delivery_date": "2025-04-01",
    "status": "Pending",
    "remarks": "Urgent delivery required",
    "contact_person_name": "Michael Johnson",
    "contact_person_email": "michael.johnson@example.com",
    "contact_person_phone": "+1-9876543210",
    "project_name": "Green Energy Project",
    "item_details": [
        {
            "item_id": 101,
            "description": "Solar Panels",
            "quantity": 50,
            "unit_price": 3000.00,
            "total_price": 150000.00
        }
    ],
    "work_order_issue_date": "2025-03-15",
    "instructions_for_delivery": "Deliver before noon",
    "critical_notes": "Handle with care",
    "logs": {}
    }
    """
    data = request.get_json()
    try:
        # first get the customer name
        customerName = getCustomerName(data["customerid"])

        data["customerName"] = customerName

        # then create the PO in the database
        createPODB(data)

        return jsonify({"message": "PO created successfully"})
    
    except Exception as e:
        logging.error(f"An error occurred while creating PO: {e}")
        return jsonify({"error": str(e)})

def fetchWO():
    """
    This function fetches a particular work order from the database based on the work order number.
    """

    try:
        workOrderNumber = request.args.get("workOrderNumber")

        # first fetch the work order from the database
        workOrder = fetchWO(workOrderNumber)

        return jsonify({"workOrder": workOrder})
    
    except Exception as e:
        logging.error(f"An error occurred while fetching work order: {e}")
        return jsonify({"error": str(e)})

def fetchProductionSlip():
    """
    This function fetches a particular production slip from the database based on the work order number.
    """

    try:
        workOrderNumber = request.args.get("workOrderNumber")

        # first fetch the production slip from the database
        productionSlip = fetchProductionSlipDB(workOrderNumber)

        return jsonify({"productionSlip": productionSlip})
    
    except Exception as e:
        logging.error(f"An error occurred while fetching production slip: {e}")
        return jsonify({"error": str(e)})


def fetchPo():
    """
    This function fetches a particular PO from the database based on the work order number.
    """

    try:
        workOrderNumber = request.args.get("workOrderNumber")

        # first fetch the PO from the database
        po = fetchPoDB(workOrderNumber)

        return jsonify({"po": po})
    
    except Exception as e:
        logging.error(f"An error occurred while fetching PO: {e}")
        return jsonify({"error": str(e)})


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
        pendingPOs = getPendingPOsDB()

        return jsonify({"pendingPOs": pendingPOs})

    except Exception as e:
        logging.error(f"An error occurred while fetching pending POs: {e}")
        return jsonify({"error": str(e)})