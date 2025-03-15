from dataControllers.cursor import cursor
import logging

def getVendorName(data):
    """
    Fetches a vendor name from the database on given vendor id.

    Example Input:
    {
        "vendorsid": "2"
    }

    Args:
        data (dict): Dictionary containing vendor name.

    Returns:
        dict: Vendor records or an error message.
    """
    try:
        # Execute SQL query
        cursor.execute("SELECT vendorName FROM vendors WHERE vendorsid = %s", (data,))
        vendors = cursor.fetchone()

        # If no vendors found, return a message
        if not vendors:
            return {"message": "No vendors found with that id"}

        return vendors["vendorName"]

    except Exception as e:
        logging.error(f"An error occurred while fetching vendors: {e}")
        return {"error": str(e)}
