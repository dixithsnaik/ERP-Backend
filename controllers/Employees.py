from dataControllers import Employees
from flask import request, jsonify
import logging
from typing import List, Dict, Any

def getEmployees():
	"""
	Fetches all employee records from the database.
	Args:
		None
	Returns:
		dict: List of employee records OR { "error": "Detailed error message" }	
	"""
	return Employees.getEmployees()

def recruitEmployee():
	"""
	Inserts employee record into the database from a employee object.
	Example Input:
	{
		"Name": "Alice Smith",
		"EmailAddress": "alice@example.com",
		"PhoneNumber": "+9876543210",
		"PermanentWorkType": "Full-Time",
		"TemporaryWorkType": null,
		"WorkType": "Project Manager",
		"AddressLine1": "456 Business St",
		"AddressLine2": "Suite 300",
		"City": "San Francisco",
		"State": "CA",
		"PinCode": "94105",
		"DateOfJoining": "2024-03-10"
	}
	Agrs:
		None (Reads JSON data from request)
	Returns:	
		Dict[str, Any]: JSON response containing either:
			- "createdEmployee": List of inserted employee records
			- "error": Error message in case of failure
	"""
	try:
		data = request.json
		if not isinstance(data, dict):
			return {"error": "Invalid data format. Expected a employee object."}, 400

		created_employee = Employees.recruitEmployee(data)

		if "error" in created_employee:
			return created_employee, 400

		return {"createdEmployee": created_employee}, 201

	except Exception as e:
		logging.error(f"An error occurred while creating employees: {e}")
		return {"error": str(e)}
	
def layoffEmployee():
	"""
	Deletes employee record from the database.
	Example Input:
	{
		"EmployeeID": 1,
		"ReasonForLayoff": "Company downsizing",
		"DateOfLayoff": "2025-03-14T11:30:25Z"
	}
	Args:
		None (Reads JSON data from request)
	Returns:
		Dict[str, Any]: JSON response containing either:
			- "deletedEmployee": List of deleted employee records
			- "error": Error message in case of failure
	"""
	try:
		data = request.json
		if not data:
			return {"error": "No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected a object with employee id and reason for layoff"}
		
		deleted_employee = Employees.layoffEmployee(data)
		return {"deletedEmployee": deleted_employee}

	except Exception as e:
		logging.error(f"An error occurred while laying off employees: {e}")
		return {"error": str(e)}

def updateRoleEmployee():
	"""
	Updates employee role in the database.
	Example Input:
	{
		"EmployeeID": 1,
		"WorkType": "user"
	}
	Args:
		None (Reads JSON data from request)
	Returns:
		Dict[str, Any]: JSON response containing either:
			- "updatedEmployee": List of updated employee records
			- "error": Error message in case of failure
	"""
	try:
		data = request.json
		if not data:
			return {"error":"No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected a object with employee id and new role"}
		
		updated_employee = Employees.updateRoleEmployee(data)
		return {"updatedEmployee": updated_employee}

	except Exception as e:
		logging.error(f"An error occurred while updating employee role: {e}")
		return
