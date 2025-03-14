# internal imports
from dataControllers.cursor import cursor

def getCustomerName(customer_id):
    try:
        cursor.execute(f"""SELECT customerName FROM customers WHERE id={customer_id}""")
        customerName = cursor.fetchone()

        return customerName
    except Exception as e:
        logging.error(f"An error occurred while fetching customer name: {e}")
        return {"error": str(e)}