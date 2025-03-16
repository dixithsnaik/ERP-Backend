from dataControllers import PurchaseOrdersOut
from flask import request, jsonify
import logging
from typing import List, Dict, Any

def getAll():
	"""
	Fetches all Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of Purchase Orders Outwards records OR { "error": "Detailed error message" }	
	"""
	return PurchaseOrdersOut.getAll()

def getPending():
	"""
	Fetches all pending Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of pending Purchase Orders Outwards records OR { "error": "Detailed error message" }"
	"""
	return PurchaseOrdersOut.getPending()

def getApproved():
	"""
	Fetches all approved Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of approved Purchase Orders Outwards records OR { "error": "Detailed error message" }"
	"""
	return PurchaseOrdersOut.getApproved()

def getRejected():
	"""
	Fetches all rejected Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of rejected Purchase Orders Outwards records OR { "error": "Detailed error message" }"
	"""
	return PurchaseOrdersOut.getRejected()

def fetch():
	"""
	Fetches a specific Purchase Order Outwards record from the database.
	Args:
		None
	Returns:
		dict: Single Purchase Order Outwards record OR { "error": "Detailed error message" }
	"""
	try:
		po_out_id = request.args.get('pooutid')
		print(po_out_id)
		return PurchaseOrdersOut.fetch(po_out_id)
	except Exception as e:
		logging.error(f"An error occurred while fetching Purchase Order Outwards: {e}")
		return {"error": str(e)}

def createPOO():
	"""
	Creates a new Purchase Order Outwards record in the database.
	Args:
		None (Reads JSON data from request)
	Returns:
		Dict[str, Any]: JSON response containing either:
			- "success": Success message in case of successful creation
			- "error": Error message in case of failure
	"""
	try:
		data = request.json
		if not isinstance(data, dict):
			return {"error": "Invalid data format. Expected a Purchase Order Outwards object."}, 400

		created_po_out = PurchaseOrdersOut.createPOO(data)

		if "error" in created_po_out:
			return created_po_out, 400

		return {"success": created_po_out}, 201

	except Exception as e:
		logging.error(f"An error occurred while creating Purchase Order Outwards: {e}")
		return {"error": str(e)}

def updatePOO():
	"""
	Updates a Purchase Order Outwards record in the database.
	Args:
		None (Reads JSON data from request)
	Returns:
		Dict[str, Any]: JSON response containing either:
			- "success": Success message in case of successful update
			- "error": Error message in case of failure
	"""
	try:
		data = request.json
		if not isinstance(data, dict):
			return {"error": "Invalid data format. Expected a Purchase Order Outwards object."}, 400

		updated_po_out = PurchaseOrdersOut.updatePOO(data)

		if "error" in updated_po_out:
			return updated_po_out, 400

		return {"success": updated_po_out}, 200

	except Exception as e:
		logging.error(f"An error occurred while updating Purchase Order Outwards: {e}")
		return {"error": str(e)}
	
def updateStatusPOO():
	"""
	Updates the status of a Purchase Order Outwards record in the database.
	Args:
		None (Reads JSON data from request)
	Returns:
		Dict[str, Any]: JSON response containing either:
			- "success": Success message in case of successful status update
			- "error": Error message in case of failure
	"""
	try:
		data=request.json
		if not data:
			return {"error": "No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected an object with Purchase Order Outwards data"}

		updated_status = PurchaseOrdersOut.updateStatusPOO(data)

		if "error" in updated_status:
			return updated_status, 400

		return {"success": updated_status}, 200
	except Exception as e:
		logging.error(f"An error occurred while updating Purchase Order Outwards status: {e}")
		return {"error": str(e)}