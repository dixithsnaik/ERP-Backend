from dataControllers.cursor import cursor, connection
import logging
import json
from datetime import datetime

def getAll():
	"""
	Fetches all Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of Purchase Orders Outwards records OR { "error": "Detailed error message" }    
	"""
	try:
		cursor.execute("SELECT * FROM po_outwards")
		users = cursor.fetchall()
		return users
	except Exception as e:
		logging.error(f"An error occurred while fetching Purchase Orders Outwards: {e}")
		return {"error": str(e)}

def getPending():
	"""
	Fetches all pending Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of pending Purchase Orders Outwards records OR { "error": "Detailed error message" }    
	"""
	try:
		cursor.execute("SELECT * FROM po_outwards WHERE status = 'pending'")
		users = cursor.fetchall()
		return users
	except Exception as e:
		logging.error(f"An error occurred while fetching pending Purchase Orders Outwards: {e}")
		return {"error": str(e)}

def getApproved():
	"""
	Fetches all approved Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of approved Purchase Orders Outwards records OR { "error": "Detailed error message" }    
	"""
	try:
		cursor.execute("SELECT * FROM po_outwards WHERE status = 'approved'")
		users = cursor.fetchall()
		return users
	except Exception as e:
		logging.error(f"An error occurred while fetching approved Purchase Orders Outwards: {e}")
		return {"error": str(e)}

def getRejected():
	"""
	Fetches all rejected Purchase Orders Outwards records from the database.
	Args:
		None
	Returns:
		dict: List of rejected Purchase Orders Outwards records OR { "error": "Detailed error message" }    
	"""
	try:
		cursor.execute("SELECT * FROM po_outwards WHERE status = 'rejected'")
		users = cursor.fetchall()
		return users
	except Exception as e:
		logging.error(f"An error occurred while fetching rejected Purchase Orders Outwards: {e}")
		return {"error": str(e)}
	
def fetch(po_out_id):
	"""
	Fetches a single Purchase Order Outwards record from the database.
	Args:
		None
	Returns:
		dict: List of Purchase Orders Outwards records OR { "error": "Detailed error message" }    
	"""
	try:	
		cursor.execute("SELECT * FROM po_outwards WHERE pooutid = %s", (po_out_id,))
		users = cursor.fetchall()
		return users
	except Exception as e:
		logging.error(f"An error occurred while fetching Purchase Orders Outwards: {e}")
		return {"error": str(e)}

def createPOO(data):
    """
    Creates a new Purchase Order Outwards record in the database.

    Args:
        data (dict): Dictionary containing PO Outwards details.

    Returns:
        dict: Success or error message.
    """
    try:
        if not data:
            return {"error": "No data provided"}
        if not isinstance(data, dict):
            return {"error": "Expected an object with PO Outwards data"}

        # Convert boolean values to integers
        data["status"] = int(data.get("status", 0))
        data["approval_status"] = int(data.get("approval_status", 0))
        data["jobwork"] = int(data.get("jobwork", 0))

        # Convert ISO format date to MySQL format (if needed)
        for date_key in ["poout_date", "delivery_date"]:
            if date_key in data and isinstance(data[date_key], str):
                try:
                    data[date_key] = datetime.strptime(data[date_key], "%Y-%m-%d").date()
                except ValueError:
                    return {"error": f"Invalid date format for {date_key}. Use YYYY-MM-DD."}

        # Convert JSON field to string
        data["itemDetails"] = json.dumps(data.get("itemDetails", []))

        # Construct SQL query dynamically
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO po_outwards ({columns}) VALUES ({placeholders})"

        cursor.execute(query, values)
        connection.commit()

        return {"success": True, "message": "Purchase Order Outwards created successfully"}
    
    except Exception as e:
        logging.error(f"An error occurred while creating Purchase Order Outwards: {e}")
        return {"error": str(e)}
	
def updatePOO(data):
	"""
	Updates an existing Purchase Order Outwards record in the database.
	Agrs:
		data (dict): Dictionary containing PO Outwards details.
	Returns:
		dict: Success or error message.
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected an object with PO Outwards data"}
		
		# Convert boolean values to integers
		data["status"] = int(data.get("status", 0))
		data["approval_status"] = int(data.get("approval_status", 0))
		data["jobwork"] = int(data.get("jobwork", 0))
		
		# Convert ISO format date to MySQL format (if needed)
		for date_key in ["poout_date", "delivery_date"]:
			if date_key in data and isinstance(data[date_key], str):
				try:
					data[date_key] = datetime.strptime(data[date_key], "%Y-%m-%d").date()
				except ValueError:
					return {"error": f"Invalid date format for {date_key}. Use YYYY-MM-DD."}
		
		# Convert JSON field to string
		data["itemDetails"] = json.dumps(data.get("itemDetails", []))
		
		# Construct SQL query dynamically
		columns = ", ".join(data.keys())
		placeholders = ", ".join(["%s"] * len(data))
		values = tuple(data.values())
		
		query = f"UPDATE po_outwards SET {columns} WHERE pooutid = {data['pooutid']}"
		
		cursor.execute(query, values)
		connection.commit()
		
		return {"success": True, "message": "Purchase Order Outwards updated successfully"}
	except Exception as e:
		logging.error(f"An error occurred while updating Purchase Order Outwards: {e}")
		return {"error": str(e)}

def updateStatusPOO(data):
	"""
	Updates the status of a Purchase Order Outwards record in the database.
	Agrs:
		data (dict): Dictionary containing PO Outwards details.
	Returns:
		dict: Success or error message.
	"""
	try:
		if not data:
			return {"error": "No data provided"}
		if not isinstance(data, dict):
			return {"error": "Expected an object with PO Outwards data"}
		
		# Construct SQL query dynamically
		query = f"UPDATE po_outwards SET status = '{data['status']}' WHERE pooutid = {data['pooutid']}"
		
		cursor.execute(query)
		connection.commit()
		
		return {"success": True, "message": "Purchase Order Outwards status updated successfully"}
	except Exception as e:
		logging.error(f"An error occurred while updating Purchase Order Outwards status: {e}")
		return {"error": str(e)}

