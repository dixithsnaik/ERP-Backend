

# internal imports
from dataControllers.cursor import cursor

def getCompanyDetailsDB():
    """
    This function fetches the company details from the database.
    The following columns are fetched:
    "company_name": "Tech Innovations Pvt Ltd",
    "company_id": 1,
    "email_address": "info@techinnovations.com",
    "phone_number": "+91-9876543210",
    "address_line1": "123, Tech Park",
    "address_line2": "Electronic City",
    "gst_number": "29ABCDE1234F1Z5",
    "city": "Bangalore",
    "state": "Karnataka",
    "pin_code": "560100",
    "gst_registration_number": "29ABCDE1234F1Z5",
    "gst_registration_type": "Regular"
    """

    # fetch the mentioned columns from mthe companyDetails table
    cursor.execute("""SELECT company_name,company_id, email_address, phone_number, address_line1,  address_line2, gst_number, city, state, pin_code, gst_registration_number,gst_registration_type FROM companyDetails""")
    companyDetails = cursor.fetchall()
    return companyDetails

def updateCompanyDetailsDB(data):
    """
    This function updates(patch) the company details in the companyDetails table of database. It updates those columns only which are present in the data input.
    Example-
    {
    "company_id": 1,
    "company_name": "Updated Company Name",
    "email_address": "updatedemail@example.com",
    "phone_number": "9876543210",
    "address_line1": "Updated Address Line 1",
    "address_line2": "Updated Address Line 2",
    "gst_number": "GST123456789",
    "city": "Updated City",
    "state": "Updated State",
    "pin_code": "560001",
    "gst_registration_number": "GSTREG987654321",
    "gst_registration_type": "Regular"
    }
    """

    # update the company details in the companyDetails table
    query = "UPDATE companyDetails SET "
    data_to_put = []
    for key in data.keys():
        if key != "company_id":
            query += key + " = %s, "
            data_to_put.append(data[key])
    query = query[:-2] + " WHERE company_id = %s"
    data_to_put.append(data["company_id"])
    cursor.execute(query, data_to_put)
    return {"message": "Company details updated successfully."}


    