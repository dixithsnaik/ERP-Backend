from dataControllers.cursor import cursor, connection
import logging
import json
from datetime import datetime

def getVendors():
    """
    Fetches all vendor records from the database.
    Args:
        None
    Returns:
        dict: List of vendor records OR { "error": "Detailed error message" }
    """
    try:
        cursor.execute("SELECT vendorName, emailAddress, phoneNumber, addressLine1, addressLine2, gstNumber, city, state, pinCode FROM vendors")
        users = cursor.fetchall()
        return users
    except Exception as e:
        logging.error(f"An error occurred while fetching vendors: {e}")
        return {"error": str(e)}

def addVendors(data):
    """This function creates vendors in the database, from a given list of vendor objects. Handles all data types.

    Args:
        data (list): List of dictionaries, each representing a vendor object.

    Returns:
        dict: { "success": True, "message": "Vendors created successfully" } OR
              { "error": "Detailed error message" }
    """
    try:
        if not data:
            return {"error": "No data provided"}
        
        if not isinstance(data, list):
            return {"error": "Expected a list of vendor objects"}

        insert_queries = []  # Store queries for batch execution

        for vendor in data:
            if not isinstance(vendor, dict):
                continue  # Skip invalid entries
            
            # Generate dynamic column names and placeholders
            columns = ', '.join(vendor.keys())
            placeholders = ', '.join(['%s'] * len(vendor))
            values = []

            for key, value in vendor.items():
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

            query = f"INSERT INTO vendors ({columns}) VALUES ({placeholders})"
            insert_queries.append((query, tuple(values)))  # Store queries and values
        
        # Execute queries one by one
        for query, values in insert_queries:
            try:
                cursor.execute(query, values)
            except Exception as e:
                logging.error(f"Failed to insert vendor: {e}")
                return {"error": f"Database insertion failed: {e}"}

        cursor.commit()  # Commit only after all insertions succeed
        return {"success": True, "message": "Vendors created successfully"}

    except Exception as e:
        logging.error(f"An error occurred while adding vendors: {e}")
        return {"error": str(e)}

def updateVendor(data):
    """This Function updates a vendor in the database, from a given list of vendor objects.
    Example:
    {
        "vendorsid": 1,                                  INT
        "vendorName": "New Vendor Name",                 VARCHAR(255)
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
        data (dict): Dictionary representing a vendor object to be updated.
    Returns:
        Dict[str, Any]: JSON response containing either:
            - "updatedVendor": Updated vendor record
            - "error": Error message in case of failure
    """
    try:
        if not data:
            return {"error": "No data provided"}
        
        if not isinstance(data, dict):
            return {"error": "Expected a vendor object"}

        # Generate dynamic column names and placeholders
        columns = ', '.join([f"{key} = %s" for key in data.keys()])
        values = list(data.values())
        values.append(data["vendorsid"])  # Add vendor ID to the end for WHERE clause

        query = f"UPDATE vendors SET {columns} WHERE vendorsid = %s"
        cursor.execute(query, tuple(values))
        connection.commit()

        return data
    except Exception as e:
        logging.error(f"An error occurred while updating vendor: {e}")
        return {"error": str(e)}
