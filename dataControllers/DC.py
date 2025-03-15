from dataControllers.cursor import cursor, connection
import logging
import json
from datetime import datetime

def getAllDC():
	"""
	Fetches all DC records from the database.
	Args:
		None
	Returns:
		dict: List of DC records OR { "error": "Detailed error message" }    
	"""
	try:
		cursor.execute("SELECT * FROM DC")
		dc = cursor.fetchall()
		return dc
	except Exception as e:
		logging.error(f"An error occurred while fetching DC: {e}")
		return {"error": str(e)}
	
def createDC(data):
	"""
	Creates a new DC record in the database.
	Args:
		None
	Returns:
		dict: { "success": True, "message": "DC created successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		
		if not isinstance(data, dict):
			return {"error": "Expected a DC object"}
			
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
		
		# Insert the record into the database
		query = f"INSERT INTO DC ({columns}) VALUES ({placeholders})"
		cursor.execute(query, tuple(values))
		connection.commit()
		return {"success": True, "message": "DC created successfully"}
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
	try:
		cursor.execute("SELECT * FROM DC WHERE dc_status = '0'")
		dc = cursor.fetchall()
		return dc
	except Exception as e:
		logging.error(f"An error occurred while fetching open DC: {e}")
		return {"error": str(e)}
	
def approvedDC():
	"""
	Fetches all approved DC records from the database.
	Args:
		None
	Returns:
 		dict: List of approved DC records OR { "error": "Detailed error message" }"
	"""
	try:
		cursor.execute("SELECT * FROM DC WHERE dc_status = '1'")
		dc = cursor.fetchall()
		return dc
	except Exception as e:
		logging.error(f"An error occurred while fetching approved DC: {e}")
		return {"error": str(e)}
	
def updateDC(data):
	"""
	Updates a DC record in the database.
	Args:
		data (dict): DC object to be updated.
	Returns:
		dict: { "success": True, "message": "DC updated successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		
		if not isinstance(data, dict):
			return {"error": "Expected a DC object"}
			
		# Generate dynamic column names and placeholders
		columns = ', '.join([f"{key} = %s" for key in data.keys()])
		values = list(data.values())
		values.append(data["dcid"])	
		query = f"UPDATE DC SET {columns} WHERE dcid = %s"
		cursor.execute(query, tuple(values))
		connection.commit()
		return {"success": True, "message": "DC updated successfully"}
	except Exception as e:
		logging.error(f"An error occurred while updating DC: {e}")
		return {"error": str(e)}

def updateStatusDC(data):
	"""
	Updates the status of a DC record in the database.
	Args:
		data (dict): DC object with status to be updated.
	Returns:
		dict: { "success": True, "message": "DC status updated successfully" } OR
			  { "error": "Detailed error message" }
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		
		if not isinstance(data, dict):
			return {"error": "Expected a DC object"}
			
		# Generate dynamic column names and placeholders
		columns = ', '.join([f"{key} = %s" for key in data.keys()])
		values = list(data.values())
		values.append(data["dcid"])	
		query = f"UPDATE DC SET {columns} WHERE dcid = %s"
		cursor.execute(query, tuple(values))
		connection.commit()
		return {"success": True, "message": "DC status updated successfully"}
	except Exception as e:
		logging.error(f"An error occurred while updating DC status: {e}")
		return {"error": str(e)}
