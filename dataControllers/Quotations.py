import json

from dataControllers.cursor import cursor

def updateQuotationDB(data):
    """
    This is db function to update a quotation in the database.
    It will only update the keys given to it and not all the keys.
    """

    query = "UPDATE quotation SET "

    for key in data.keys():
        if key == "quotationid":
            continue    # Skip the quotationid key
        query += key + " = %s, "

    query = query[:-2]  # Remove the trailing comma and space
    query += " WHERE quotationid = %s"

    data_to_put = list(data.values())
    quotationid = data_to_put.pop(0)  # Remove the quotationid from the data list

    for i in range(len(data_to_put)):
        if type(data_to_put[i]) == dict:
            data_to_put[i] = json.dumps(data_to_put[i])

    print(data_to_put)
    print(query)

    print(query.count("%s"))
    print(len(data_to_put)+1)

    cursor.execute(query, data_to_put + [quotationid])

    return "Quotation updated successfully"

def createQuotationDB(data):
    """
    This is db function to create a quotation in the database.
    """

    # inset the data from the request into the database
    #create a query string using the data from the request

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

def approvalStatusDB(quotationid, AdminApproved):
    """
    This is db function to update the approval status of a quotation in the database.
    the input will be 
    {
    "quotationid": "INT",
    "AdminApproved":"BOOLEAN"
    }
    in post request
    we will update the AdminApproved column in the database
    """

    # update the approval status of the quotation in the database
    cursor.execute("""UPDATE quotation SET AdminApproved = %s WHERE quotationid = %s""", (AdminApproved, quotationid))

    return "Approval status updated successfully"

def rejectedQuotationDB():
    """
    This is db function to reject a quotation in the database.
    {
  "quotations": [
            {
            "quotationid": 502,
            "customerid": 102,
            "name": "Alice Smith",
            "emailAddress": "alice.smith@example.com",
            "phoneNumber": "9876543210",
            "deliveryDate": "2025-04-20",
            "AdminApproved":false,
            "itemDetails": {
                "items": [
                {
                    "itemDescription": "Voltage Regulator",
                    "partNumber": "VR-9012",
                    "quantity": 20,
                    "unitRateINR": 300,
                    "note": "For power supply circuits"
                }
                ],
                "notes": "Urgent delivery required."
            }
            }
        ]
        }
    """

    # getting all the quotations which are rejected by the admin
    cursor.execute("""SELECT
                        quotationid,
                        customerid,
                        name,
                        emailAddress,
                        phoneNumber,
                        deliveryDate,
                        AdminApproved,
                        itemDetails
                        FROM quotation WHERE AdminApproved = 0""")

    rejectedQuotation = cursor.fetchall()

    return rejectedQuotation

def approvedQuotationDB():
    """
    This is db function to approve a quotation in the database.
    {
  "quotations": [
            {
            "quotationid": 502,
            "customerid": 102,
            "name": "Alice Smith",
            "emailAddress": "alice.smith@example.com",
            "phoneNumber": "9876543210",
            "deliveryDate": "2025-04-20",
            "AdminApproved": true,
            "itemDetails": {
                "items": [
                {
                    "itemDescription": "Voltage Regulator",
                    "partNumber": "VR-9012",
                    "quantity": 20,
                    "unitRateINR": 300,
                    "note": "For power supply circuits"
                }
                ],
                "notes": "Urgent delivery required."
            }
            }
        ]
        }
    """
    
    # getting all the quotations which are approved by the admin
    cursor.execute("""SELECT
                        quotationid,
                        customerid,
                        name,
                        emailAddress,
                        phoneNumber,
                        deliveryDate,
                        AdminApproved,
                        itemDetails
                        FROM quotation WHERE AdminApproved = 1""")

    approvedQuotation = cursor.fetchall()

    return approvedQuotation



def getPendingApprovalQuotationsDB():
    """
    This is db function to fetch all quotations pending approval from the database.
    {
        "quotationid": "INT",
        "customer_name": "STRING",//customer table
        "rfqid": "INT",
        "name": "VARCHAR(255)",
        "emailAddress": "VARCHAR(255)",
        "phoneNumber": "VARCHAR(15)",
        "termsAndConditions": "TEXT",
        "paymentTerms": "TEXT",
        "taxAndDuties": "TEXT",
        "briefDescription": "TEXT",
        "deliveryDate": "DATE",
        "packageAndForwarding": "TEXT",
        "createdBy": "INT",
        "AdminApproved": "BOOLEAN",
        "log": "JSON",
        "itemDetails": "JSON",
        "created_at": "TIMESTAMP",
        "updated_at": "TIMESTAMP"
    }
    """

    # fetch all quotations pending approval from the database
    cursor.execute("""SELECT 
                        quotationid,
                        customerid,
                        rfqid,
                        name,
                        emailAddress,
                        phoneNumber,
                        termsAndConditions,
                        paymentTerms,
                        taxAndDuties,
                        briefDescription,
                        deliveryDate,
                        packageAndForwarding,
                        createdBy,
                        AdminApproved,
                        log,
                        itemDetails,
                        created_at,
                        updated_at
                      FROM quotation WHERE AdminApproved = NULL""")
    pendingApprovalQuotations = cursor.fetchall()

    return pendingApprovalQuotations

def getAllQuotationsDB():
    """
    This is db function to fetch all quotations from the database.
    "quotations": [
            {
            "quotationid": 501,
            "customerid": 101,
            "name": "John Doe",
            "emailAddress": "john.doe@example.com",
            "phoneNumber": "1234567890",
            "deliveryDate": "2025-04-15",
            "AdminApproved": null,
            "itemDetails": {
                "items": [
                {
                    "itemDescription": "Microcontroller Unit",
                    "partNumber": "MCU-1234",
                    "quantity": 10,
                    "unitRateINR": 1500,
                    "note": "High-performance MCU for industrial use"
                }
                ],
                "notes": "Bulk order, special discount applied."
            }
            }
        ]
        }
    """

    # fetch all quotations from the database
    cursor.execute("""SELECT 
                        quotationid,
                        customerid,
                        name,
                        emailAddress,
                        phoneNumber,
                        deliveryDate,
                        AdminApproved,
                        itemDetails
                      FROM quotation""")
    allQuotations = cursor.fetchall()

    return allQuotations

def getUnapprovedQuotationsDB():
    """
    This is db function to fetch all unapproved quotations from the database.
    {
    "quotationid": "INT",
    "customer_name": "INT", //getfrom customet table
    "rfqid": "INT",
    "name": "VARCHAR(255)",
    "deliveryDate": "DATE",
    "createdBy":"string", // get from users(userid) -> username
    "AdminApproved": "BOOLEAN",
    }
    """

    # fetch all unapproved quotations from the database
    cursor.execute("""SELECT 
                        quotationid,
                        customerid,
                        rfqid,
                        name,
                        deliveryDate,
                        createdBy,
                        AdminApproved
                      FROM quotation WHERE AdminApproved = 0""")
    unapprovedQuotations = cursor.fetchall()

    return unapprovedQuotations