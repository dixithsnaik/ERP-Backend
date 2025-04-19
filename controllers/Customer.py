from dataControllers import Customer
from flask import request, jsonify
import logging
from typing import List, Dict, Any

def getCustomers():
    """
    Fetches all customer records from the database.
    Args:
		None
    Returns:
		dict: List of customer records OR { "error": "Detailed error message" }
    """
    return Customer.getCustomers()

def addCustomer() -> Dict[str, Any]:
    """
    Inserts multiple customer records into the database from a given list of customer objects.

    Example Input:
    {
		"customerId": "21",								# INT
		"customerName": "Acme Corporation",				# VARCHAR(255)
		"emailAddress": "contact@acmecorp.com", 		# VARCHAR(255)
		"phoneNumber": "1234567890", 					# VARCHAR(10)
		"addressLine1": "123 Business Avenue",			# VARCHAR(255)
		"addressLine2": "Suite 456", 					# VARCHAR(255)
		"gstNumber": "29AADCB2230M1ZT", 				# VARCHAR(15)
		"city": "Bangalore", 							# VARCHAR(255)
		"state": "Karnataka", 							# VARCHAR(255)
		"pinCode": "560001" 							# VARCHAR(6)
        "created_at": "2025-03-14T11:30:25Z" 			# TIMESTAMP
        "updated_at": "2025-03-14T11:30:25Z" 			# TIMESTAMP
	}

    Args:
        None (Reads JSON data from request)

    Returns:
        Dict[str, Any]: JSON response containing either:
            - "createdcustomers": List of inserted customer records
            - "error": Error message in case of failure
    """
    try:
        # Validate JSON input
        data = request.json
        if not isinstance(data, dict):
            return {"error": "Invalid data format. Expected a customer object."}, 400

        # Insert customers into the database
        created_customer = Customer.addCustomer(data)

        # Check if customers.addcustomers() returned an error
        if "error" in created_customer:
            return created_customer, 400

        return {"createdcustomers": created_customer}, 201

    except Exception as e:
        logging.error(f"An error occurred while creating customers: {e}")
        if "1062" in str(e):  
            return {"error": "Duplicate entry - This customer already exists."}, 409  # 409 Conflict
        return {"error": str(e)}, 400


def updateCustomer():
	"""This Function updates a customer in the database, from a given list of customer objects.
	  Example:"
	  {
		"customersId": 1, 								INT
		"customerName": "New customer Name", 				VARCHAR(255)
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
			- "updatedcustomer": Updated customer record
			- "error": Error message in case of failure
	"""
	try:
		# Validate JSON input
		data = request.json
		if not isinstance(data, dict):
			return {"error": "Invalid data format. Expected a customer object."}, 400

		# Update customer in the database
		updated_customer = Customer.updateCustomer(data)

		# Check if customers.updatecustomer() returned an error
		if "error" in updated_customer:
			return updated_customer, 400

		return {"updatedcustomer": updated_customer}, 200

	except Exception as e:
		logging.error(f"An error occurred while updating customer: {e}")
		if "1062" in str(e):
			return {"error": "Duplicate entry - This customer already exists."}, 409  # Conflict
		return {"error": str(e)}, 400
