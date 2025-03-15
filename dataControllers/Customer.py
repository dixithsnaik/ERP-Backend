from dataControllers.cursor import cursor, connection
import logging
import json
from datetime import datetime

def getCustomers():
    """
    Fetches all Customer records from the database.
    Args:
        None
    Returns:
        dict: List of Customer records OR { "error": "Detailed error message" }
    """
    try:
        cursor.execute("SELECT * FROM customer")
        users = cursor.fetchall()
        return users
    except Exception as e:
        logging.error(f"An error occurred while fetching customers: {e}")
        return {"error": str(e)}

def addCustomer(data):
    """This function creates Customers in the database, from a given list of Customer objects. Handles all data types.

    Args:
        data (dict): List of dictionaries, each representing a Customer object.

    Returns:
        dict: { "success": True, "message": "Customers created successfully" } OR
              { "error": "Detailed error message" }
    """
    try:
        if not data:
            return {"error": "No data provided"}
        
        if not isinstance(data, dict):
            return {"error": "Expected a Customer object"}

            
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
                values.append(value)  # Fallback for other data types

        query = f"INSERT INTO customer ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(query, values)
        except Exception as e:
                logging.error(f"Failed to insert Customer: {e}")
                return {"error": f"Database insertion failed: {e}"}

        connection.commit()  # Commit only after all insertions succeed
        return {"success": True, "message": "Customers created successfully"}

    except Exception as e:
        logging.error(f"An error occurred while adding Customers: {e}")
        return {"error": str(e)}

def updateCustomer(data):
    """This Function updates a Customer in the database, from a given list of Customer objects.
    Example:
    {
        "Customersid": 1,                                INT
        "CustomerName": "New Customer Name",             VARCHAR(255)
        "emailAddress": "abc@email.com",                 VARCHAR(255)
        "phoneNumber": "9876543210",                     VARCHAR(10)
        "addressLine1": "New Address Line 1",            VARCHAR(255)
        "addressLine2": "New Address Line 2",            VARCHAR(255)
        "gstNumber": "GST12345678",                      VARCHAR(15)
        "city": "New City",                              VARCHAR(255)
        "state": "New State",                            VARCHAR(255)
        "pinCode": "123456"                              VARCHAR(6)
        "updated_at": "2025-03-14T11:30:25Z"             TIMESTAMP
    }  
    Args:
        data (dict): Dictionary representing a Customer object to be updated.
    Returns:
        Dict[str, Any]: JSON response containing either:
            - "updatedCustomer": Updated Customer record
            - "error": Error message in case of failure
    """
    try:
        if not data:
            return {"error": "No data provided"}
        
        if not isinstance(data, dict):
            return {"error": "Expected a Customer object"}

        # Generate dynamic column names and placeholders
        columns = ', '.join([f"{key} = %s" for key in data.keys()])
        values = list(data.values())
        values.append(data["customerid"])  # Add Customer ID to the end for WHERE clause

        query = f"UPDATE customer SET {columns} WHERE customerid = %s"
        cursor.execute(query, tuple(values))
        connection.commit()

        return {"updatedCustomer": data}
    except Exception as e:
        logging.error(f"An error occurred while updating Customer: {e}")
        return {"error": str(e)}
