from dataControllers.cursor import cursor

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