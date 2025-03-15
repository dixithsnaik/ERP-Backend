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
                                                updatePODB,
                                                createProductionSlipDB,
                                                updateProductionSlipDB,
                                                fetchCustomerAcceptanceDB,
                                                updateCustomerAcceptanceDB
                                             )
from dataControllers.Customers import getCustomerName

def updateCustomerAcceptance():
    """
    this function updates the customer acceptance of a production slip in the database.
    {
        "workordernumber": 1,
        "customer_acceptance_status": 1,
        "reason_for_rejection": "Throughout beyond consumer resource it myself. Picture office military knowledge military seven. Company dream drive better purpose."
        .. other fields
    }
    """

    data = request.get_json()
    try:
        # then update the customer acceptance in the database
        updateCustomerAcceptanceDB(data)

        return jsonify({"message": "Customer acceptance updated successfully"})
    
    except Exception as e:
        logging.error(f"An error occurred while updating customer acceptance: {e}")
        return jsonify({"error": str(e)})

def fetchCustomerAcceptance():
    """
    this function fetches all the customer acceptance, of production slips, from the database.
    """
    try:
        # first fetch all the customer acceptance from the database
        customerAcceptance = fetchCustomerAcceptanceDB()

        return jsonify({"customerAcceptance": customerAcceptance})
    
    except Exception as e:
        logging.error(f"An error occurred while fetching customer acceptance: {e}")
        return jsonify({"error": str(e)})

def updateProductionSlip():
    """
    this function updates a production slip in the database.
    {
        "account": "avinash Bell",
        "created_at": "Sat, 15 Mar 2025 13:18:28 GMT",
        "customer": "Patricia Gillespie",
        "customer_acceptance_status": 0,
        "logs": "Energy see employee pull person history free. Hospital represent spring win.\nStrategy adult speech north whatever seek. Tonight ask them watch arrive fine remain.",
        "project_engineer": "Tina Weaver, Dale Hill",
        "project_name": "Rice PLC",
        "quality_engineer": "Timothy Patterson, Dana Lee",
        "reason_for_rejection": "Throughout beyond consumer resource it myself. Picture office military knowledge military seven. Company dream drive better purpose.",
        "slip_date": "Sun, 23 Feb 2025 00:00:00 GMT",
        "slip_number": 3,
        "special_instruction": "Can media sound study within amount else. Traditional cold affect smile and give. Language I view nor young.\nCourt chance Mrs public either. Road artist some whom use already.",
        "store": "Andrewmouth",
        "workordernumber": 1
    }
    """

    data = request.get_json()
    try:
        # then update the production slip in the database
        updateProductionSlipDB(data)

        return jsonify({"message": "Production slip updated successfully"})
    
    except Exception as e:
        logging.error(f"An error occurred while updating production slip: {e}")
        return jsonify({"error": str(e)})

def createProductionSlip():
    """
    this function creates a new production slip in the database.
    {
        "account": "Katelyn Bell",
        "created_at": "Sat, 15 Mar 2025 13:18:28 GMT",
        "customer": "Patricia Gillespie",
        "customer_acceptance_status": 0,
        "logs": "Energy see employee pull person history free. Hospital represent spring win.\nStrategy adult speech north whatever seek. Tonight ask them watch arrive fine remain.",
        "project_engineer": "Tina Weaver, Dale Hill",
        "project_name": "Rice PLC",
        "quality_engineer": "Timothy Patterson, Dana Lee",
        "reason_for_rejection": "Throughout beyond consumer resource it myself. Picture office military knowledge military seven. Company dream drive better purpose.",
        "slip_date": "Sun, 23 Feb 2025 00:00:00 GMT",
        "slip_number": 3,
        "special_instruction": "Can media sound study within amount else. Traditional cold affect smile and give. Language I view nor young.\nCourt chance Mrs public either. Road artist some whom use already.",
        "store": "Andrewmouth",
        "workordernumber": 1
    }
    """

    data = request.get_json()
    try:
        # then create the production slip in the database
        createProductionSlipDB(data)

        return jsonify({"message": "Production slip created successfully"})
    
    except Exception as e:
        logging.error(f"An error occurred while creating production slip: {e}")
        return jsonify({"error": str(e)})

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