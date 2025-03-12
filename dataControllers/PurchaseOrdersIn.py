# internal imports
from dataControllers.cursor import cursor

def getPendingPOs():
    try:
        cursor.execute("""SELECT workordernumber,
                                 po_number,
                                 customer,
                                 po_date,
                                 amount,
                                 product_engineers,
                                 quality_engineers,
                                 delivery_date,
                                 status,
                                 remarks
                         FROM purchase_orders WHERE status='Pending'
                         """)
        pendingPOs = cursor.fetchall()

        return pendingPOs
    except Exception as e:
        logging.error(f"An error occurred while fetching pending POs: {e}")
        return {"error": str(e)}