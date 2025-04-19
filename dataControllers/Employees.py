from dataControllers.cursor import cursor, connection
import logging
import json
from datetime import datetime

def getEmployees():
    """
    Fetches all Employees records from the database.
    Args:
        None
    Returns:
        dict: List of Employees records OR { "error": "Detailed error message" }
    """
    try:
        cursor.execute("SELECT * FROM EmployeeRecords")
        users = cursor.fetchall()
        return users
    except Exception as e:
        logging.error(f"An error occurred while fetching Employees: {e}")
        return {"error": str(e)}

def recruitEmployee(data):
	"""This function creates Employees in the database, from a given list of Employee objects. Handles all data types.

	Args:
		data (dict): List of dictionaries, each representing a Employee object."
	Returns:
		dict: { "success": True, "message": "Employees created successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		
		if not isinstance(data, dict):
			return {"error": "Expected a Employee object"}
			
		# Generate dynamic column names and placeholders
		columns = ', '.join(data.keys())
		placeholders = ', '.join(['%s'] * len(data))
		values = []
		for key, value in data.items():
			if isinstance(value, bool):
				values.append(int(value))  # Convert True/False to 1/0
			elif isinstance(value, (int, float)):  
				values.append(value)  # Keep integers and floats as is
			elif isinstance(value, dict):  
				values.append(json.dumps(value))  # Convert dict to JSON string
			elif isinstance(value, str):
				# Convert ISO timestamp format if it looks like one
				try:
					if value.endswith("Z") and "T" in value:
						dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
						values.append(dt.strftime("%Y-%m-%d %H:%M:%S"))  # Convert to MySQL format
					else:
						values.append(value)  # Keep as regular string
				except ValueError:
					values.append(value)  # If not a valid timestamp, keep as string
			else:
				values.append(value)  # Keep as is if not any of the above types
				
		# Insert the Employee records into the database
		cursor.execute(f"INSERT INTO EmployeeRecords ({columns}) VALUES ({placeholders})", tuple(values))
		connection.commit()
		return {"success": True, "message": "Employee created successfully"}
	except Exception as e:
		logging.error(f"An error occurred while creating Employees: {e}")
		return {"error": str(e)}

def layoffEmployee(data):
	"""
	This function lays off an Employee from the database.
	Args:
		data (dict): Employee id and ReasonForLayoff to be laid off.
	Returns:
		dict: { "success": True, "message": "Employee laid off successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected a object with employee id and reason for layoff"}
		
		# Lay off the Employee from the database
		cursor.execute("DELETE FROM EmployeeRecords WHERE EmployeeID = %s", (data["EmployeeID"],))
		connection.commit()
		return {"success": True, "message": "Employee laid off successfully"}
	except Exception as e:
		logging.error(f"An error occurred while laying off Employee: {e}")
		return {"error": str(e)}

def updateRoleEmployee(data):
	"""
	This function updates a given Employee's role in the database.
	Args:
		data (dict): Employee id and new role (worktypes) to be updated.
	Returns:
		dict: { "success": True, "message": "Employee role updated successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		if not data:
			return {"error":"No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected a object with employee id and new role"}
		
		# Update the Employee role in the database
		columns = ', '.join([f"{key} = %s" for key in data.keys()])
		values = list(data.values())
		values.append(data["EmployeeID"])
		query = f"UPDATE EmployeeRecords SET {columns} WHERE EmployeeID = %s"
		cursor.execute(query, tuple(values))
		connection.commit()
		return {"success": True, "message": "Employee role updated successfully"}
	except Exception as e:
		logging.error(f"An error occurred while updating Employee role: {e}")
		return {"error": str(e)}
