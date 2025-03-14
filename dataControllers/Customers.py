import logging

# internal imports
from dataControllers.cursor import cursor

def getCustomerName(customer_id):
    try:
        print(f"customer_id: {customer_id}")
        cursor.execute(f"""SELECT customerName FROM customer WHERE customerid={customer_id}""")
        customerName = cursor.fetchone()
        return customerName["customerName"]
    except Exception as e:
        logging.error(f"An error occurred while fetching customer name: {e}")
        return {"error": str(e)}