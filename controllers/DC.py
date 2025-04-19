from dataControllers import DC
from flask import request, jsonify
import logging
from typing import List, Dict, Any

def getAllDC():
	"""
	Fetches all DC records from the database.
	Args:
		None
	Returns:
		dict: List of DC records OR { "error": "Detailed error message" }	
	"""
	return DC.getAllDC()

def createDC():
	"""
	Creates a new DC record in the database.
	Args:
		None
	Returns:
		dict: { "success": True, "message": "DC created successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:

		data = request.get_json()
		return DC.createDC(data)
	except Exception as e:
		logging.error(f"An error occurred while creating DC: {e}")
		return {"error": str(e)}
	
def openDC():
	"""
	Fetches all open DC records from the database.
	Args:
		None
	Returns:
		dict: List of open DC records OR { "error": "Detailed error message" }	
	"""
	return DC.openDC()

def approvedDC():
	"""
	Fetches all approved DC records from the database.
	Args:
		None 
	Returns:
		dict: List of approved DC records OR { "error": "Detailed error message" }
	"""
	return DC.approvedDC()

def updateDC():
	"""
	Updates a DC record in the database.
	Args:
		None 
	Returns:
		dict: { "success": True, "message": "DC updated successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		data = request.get_json()
		return DC.updateDC(data)
	except Exception as e:
		logging.error(f"An error occurred while updating DC: {e}")
		return {"error": str(e)}

def updateStatusDC():
	"""
	Updates the status of a DC record in the database.
	Args:
		None 
	Returns:
		dict: { "success": True, "message": "DC status updated successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		data = request.get_json()
		return DC.updateStatusDC(data)
	except Exception as e:
		logging.error(f"An error occurred while updating DC status: {e}")
		return {"error": str(e)}
