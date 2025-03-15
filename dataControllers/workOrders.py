from dataControllers.cursor import cursor

def fetchAllWorkOrdersDB():
    """
    This function fetches all the work orders from the  database.
    :return: A list of all the work orders
    """
    cursor.execute("""SELECT workordernumber,
                                customer,
                                product_engineers,
                                quality_engineers,
                                delivery_date,
                                status,
                                remarks
                        FROM work_orders
                        """)
    workOrders = cursor.fetchall()
    return workOrders