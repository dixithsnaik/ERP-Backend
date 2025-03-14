from dataControllers import Vendors
from flask import request, jsonify
import logging
from typing import List, Dict, Any

def getVendors():
    """
    Fetches all vendor records from the database.
    """
    return Vendors.getVendors()

def addVendors() -> Dict[str, Any]:
    """
    Inserts multiple vendor records into the database from a given list of vendor objects.

    Example Input:
    [
        {
            "vendorsid": 1,                               # INT
            "vendorName": "Global Supplies Inc.",         # VARCHAR(255)
            "emailAddress": "contact@globalsupplies.com", # VARCHAR(255)
            "phoneNumber": "9876543210",                  # VARCHAR(10)
            "addressLine1": "789 Industrial Zone",        # VARCHAR(255)
            "addressLine2": "Building C",                 # VARCHAR(255)
            "gstNumber": "33AAQPS7863L1ZO",               # VARCHAR(15)
            "city": "Mumbai",                             # VARCHAR(255)
            "state": "Maharashtra",                       # VARCHAR(255)
            "pinCode": "400001",                          # VARCHAR(6)
            "created_at": "2025-03-14T11:30:25Z",         # TIMESTAMP (ISO 8601 Format)
            "updated_at": "2025-03-14T11:30:25Z"          # TIMESTAMP (ISO 8601 Format)
        }
    ]

    Args:
        None (Reads JSON data from request)

    Returns:
        Dict[str, Any]: JSON response containing either:
            - "createdVendors": List of inserted vendor records
            - "error": Error message in case of failure
    """
    try:
        # Validate JSON input
        data = request.json
        if not isinstance(data, list):
            return {"error": "Invalid data format. Expected a list of vendor objects."}, 400

        # Insert vendors into the database
        created_vendors = Vendors.addVendors(data)

        # Check if Vendors.addVendors() returned an error
        if isinstance(created_vendors, dict) and "error" in created_vendors:
            return created_vendors, 400

        return {"createdVendors": created_vendors}, 201

    except Exception as e:
        logging.error(f"An error occurred while creating vendors: {e}")
        if "1062" in str(e):  
            return {"error": "Duplicate entry - This vendor already exists."}, 409  # 409 Conflict
        return {"error": str(e)}, 400


def updateVendor():
	"""This Function updates a vendor in the database, from a given list of vendor objects.
	  Example:"
	  {
		"vendorsid": 1, 								INT
		"vendorName": "New Vendor Name", 				VARCHAR(255)
		"emailAddress": "newemail@example.com", 		VARCHAR(255)
		"phoneNumber": "9876543210", 					VARCHAR(10) 
		"addressLine1": "New Address Line 1", 			VARCHAR(255)
		"addressLine2": "New Address Line 2",			VARCHAR(255)
		"gstNumber": "GST12345678", 					VARCHAR(15)
		"city": "New City", 							VARCHAR(255)
		"state": "New State", 							VARCHAR(255)
		"pinCode": "123456" 							VARCHAR(6)
		"updated_at": "2025-03-14T11:30:25Z" 			TIMESTAMP
	  }
	Args:
        None (Reads JSON data from request)
    Returns:
		Dict[str, Any]: JSON response containing either:
			- "updatedVendor": Updated vendor record
			- "error": Error message in case of failure
	"""
	try:
		# Validate JSON input
		data = request.json
		if not isinstance(data, dict):
			return {"error": "Invalid data format. Expected a vendor object."}, 400

		# Update vendor in the database
		updated_vendor = Vendors.updateVendor(data)

		# Check if Vendors.updateVendor() returned an error
		if isinstance(updated_vendor, dict) and "error" in updated_vendor:
			return updated_vendor, 400

		return {"updatedVendor": updated_vendor}, 200

	except Exception as e:
		logging.error(f"An error occurred while updating vendor: {e}")
		if "1062" in str(e):  
			return {"error": "Duplicate entry - This vendor already exists."}, 409  # 409 Conflict
		return {"error": str(e)}, 400
