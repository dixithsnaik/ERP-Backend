from dataControllers.cursor import cursor
import logging

def getEmployeeName(data):
	"""
	Fetches an employee record from id from the database.

	Example Input:
	{
		"EmployeeID": "2"
	}

	Args:
		data (dict): Dictionary containing employee name.

	Returns:
		dict: Employee records or an error message.
	"""
	try:
		# Execute SQL query
		cursor.execute("SELECT Name FROM EmployeeRecords WHERE EmployeeID = %s", (data,))
		employee = cursor.fetchone()

		# If no employees found, return a message
		if not employee:
			return {"message": "No employees found with that EmployeeID"}

		return employee["Name"]

	except Exception as e:
		logging.error(f"An error occurred while fetching employees: {e}")
		return {"error": str(e)}