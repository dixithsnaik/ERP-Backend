# internal imports
from dataControllers.cursor import cursor

def updatePODB(data):
    try:
        query="""UPDATE purchase_order SET """

        for key in data.keys():
            query+=key+"=%s,"

        query=query[:-1]+" WHERE workordernumber=%s"

        data_to_put=list(data.values())

        for i in range(len(data_to_put)):
            if type(data_to_put[i])==dict:
                data_to_put[i]=json.dumps(data_to_put[i])

        print(data_to_put)

        print(query)

        cursor.execute(query,data_to_put)

        return "Quotation updated successfully"

        return {"message": "PO created successfully"}
    except Exception as e:
        return {"error": str(e)}

def createPODB(data):
    try:
        query="""INSERT into quotation ("""

        for key in data.keys():
            query+=key+","

        query=query[:-1]+") VALUES ("

        for key in data.keys():
            query+="%s,"
        
        query=query[:-1]+")"

        data_to_put=list(data.values())

        for i in range(len(data_to_put)):
            if type(data_to_put[i])==dict:
                data_to_put[i]=json.dumps(data_to_put[i])

        print(data_to_put)

        print(query)

        cursor.execute(query,data_to_put)

        return "Quotation created successfully"

        return {"message": "PO created successfully"}
    except Exception as e:
        return {"error": str(e)}

def fetchWODB(workOrderNumber):
    try:
        cursor.execute("""SELECT *
                         FROM work_order WHERE workordernumber=%s
                         """, (workOrderNumber,))
        workOrder = cursor.fetchone()

        return workOrder
    except Exception as e:
        return {"error": str(e)}

def fetchProductionSlipDB(workOrderNumber):
    try:
        cursor.execute("""SELECT *
                         FROM production_slip WHERE workordernumber=%s
                         """, (workOrderNumber,))
        productionSlip = cursor.fetchone()

        return productionSlip
    except Exception as e:
        return {"error": str(e)}

def fetchPoDB(workOrderNumber):
    try:
        cursor.execute("""SELECT workordernumber,
                                 po_number,
                                 customer,
                                 po_date,
                                 amount,
                                 project_engineers,
                                 quality_engineers,
                                 delivery_date,
                                 status,
                                 remarks
                         FROM purchase_order WHERE workordernumber=%s
                         """, (workOrderNumber,))
        po = cursor.fetchone()

        return po
    except Exception as e:
        return {"error": str(e)}

def getPendingPOsDB():
    try:
        cursor.execute("""SELECT workordernumber,
                                 po_number,
                                 customer,
                                 po_date,
                                 amount,
                                 project_engineers,
                                 quality_engineers,
                                 delivery_date,
                                 status,
                                 remarks
                         FROM purchase_order WHERE status='Pending'
                         """)
        pendingPOs = cursor.fetchall()

        return pendingPOs
    except Exception as e:
        return {"error": str(e)}