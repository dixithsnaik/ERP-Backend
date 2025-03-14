from dataControllers.cursor import cursor

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
                      FROM quotation WHERE AdminApproved = 0""")
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