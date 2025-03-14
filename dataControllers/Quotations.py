from dataControllers.cursor import cursor

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