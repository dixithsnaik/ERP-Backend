import json
# internal imports
from dataControllers.cursor import cursor

def postRfqDetailsDB(data):
    """
    This is db function to post the data of a RFQ(Request for Quotataion) in the rfq table
    {
    "customerid": 123,
    "location": "Shanghai Port",
    "country": "China",
    "requestVia": "Email",
    "requestReferenceNumber": "RFQ-2025-001",
    "typeOfGoods": "Electronics, Computer Parts",
    "lastDateToSubmit": "2025-04-15",
    "contactPerson": "Jane Smith",
    "contactPersonNumber": "+86123456789",
    "contactPersonEmail": "jane.smith@company.com",
    "status": null
    }
    """
    # insert the data of a RFQ(Request for Quotataion) in the rfq table
    query="""INSERT into rfq ("""

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
        
        
    # print(query)
    # print(data_to_put)

    cursor.execute(query, data_to_put)  
    return {"message": "RFQ created successfully."} 

def fetchAllRfqDetailsDB():
    """
    This is db function to fetch all RFQs(Request for Quotataion) from the rfq table
    """
    # fetch all RFQs(Request for Quotataion) from the rfq table
    cursor.execute("""SELECT * FROM rfq""")
    rfqs = cursor.fetchall()

    return rfqs

def fetchAllRfqDetailsDB():
    """
    This is db function to fetch all pending RFQs(Request for Quotataion) from the rfq table
    """
    # pending RFQs means either the status is null or 0
    cursor.execute("""SELECT * FROM rfq WHERE status IS NULL OR status=0""")
    rfqs = cursor.fetchall()
    return rfqs