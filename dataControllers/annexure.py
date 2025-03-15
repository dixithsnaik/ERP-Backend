from dataControllers.cursor import cursor
import json

def createAnnexureDB(data):
    """
    This function creates an annexure in the annexure table of database.It takes the below columns as input:
    {
    "annexureType": "Job Work",  // here annexure Type should only either be Job Work or Purchase 
    "employeeId": 10,
    "workOrderNumber": 5,
    "vendorId": 20,
    "statusManager": null,
    "statusAdmin": null,
    "itemDetails": {
      "totalAmount": 9500.0,
      "items": [
        {
          "partNumber": "P001",
          "description": "Steel Plate",
          "qty": 10,
          "material": "Stainless Steel",
          "thicknessInMM": 5.0,
          "materialSize": "100x200",
          "unitPrice": 500.0
        },
        {
          "partNumber": "P002",
          "description": "Aluminium Sheet",
          "qty": 15,
          "material": "Aluminium",
          "thicknessInMM": 2.5,
          "materialSize": "150x300",
          "unitPrice": 300.0
        }
      ]
    }
    }
    :return: A dictionary with the status of the operation
    """

    query="""INSERT into annexure ("""

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
    
    cursor.execute(query, data_to_put)
    return {"message": "Annexure created successfully."}


def fetchAllAnnexuresDB(employeeId, workOrderNumber):
    """
    This function fetches all the annexures from the annexure table of database.
    :return: A list of all the annexures
    """
    cursor.execute("""SELECT * FROM annexure WHERE employeeId=%s AND workOrderNumber=%s""",(employeeId, workOrderNumber))
    annexures = cursor.fetchall()
    return annexures    

def fetchManagerAnnexuresDB(workOrderNumber):
    """
    This function fetches all the annexures for the given workorder number from the annexure table of database.
    :return: A list of all the annexures
    """
    cursor.execute("""SELECT * FROM annexure WHERE workordernumber=%s AND statusmanager IS NULL""",(workOrderNumber,))
    annexures = cursor.fetchall()
    return annexures

def managerApprovalStatusDB(data):
    """
    This function updates the manager's approval status of the annexure in the annexure table of database.
    the data should be in the format:
    {
    statusManagerId: 21,
    statusManager:1,
    annexureId:5,
    }
    """

    query = "UPDATE annexure SET "
    data_to_put = []
    for key in data.keys():
        if key != "annexureId":
            query += key + " = %s, "
            data_to_put.append(data[key])
    query = query[:-2] + " WHERE annexureid = %s"
    data_to_put.append(data["annexureId"])

    cursor.execute(query, data_to_put)

    return {"message": "Manager's approval status updated successfully."}

def fetchAdminAnnexuresDB():
    """
    This function fetches all the annexures to be shown the admin from the annexure table of database.
    It returns all the annexures with statusManager as 1 and statusAdmin as null.
    :return: A list of all the annexures
    """
    cursor.execute("""SELECT * FROM annexure WHERE statusManager=1 AND statusAdmin IS NULL""")
    annexures = cursor.fetchall()
    return annexures

def adminApprovalStatusDB(data):
    """
    This function updates the admin's approval status of the annexure in the annexure table of database.
    the data should be in the format:
    {
    statusAdminId: 21,
    statusAdmin:1,
    annexureId:5,
    }
    """

    query = "UPDATE annexure SET "
    data_to_put = []
    for key in data.keys():
        if key != "annexureId":
            query += key + " = %s, "
            data_to_put.append(data[key])
    query = query[:-2] + " WHERE annexureid = %s"
    data_to_put.append(data["annexureId"])

    cursor.execute(query, data_to_put)

    return {"message": "Admin's approval status updated successfully."}

def fetchApprovedAnneuxresDB():
    """
    This function fetches all approved annexures from the database.
    :return: A list of all the approved annexures
    """
    cursor.execute("""SELECT * FROM annexure WHERE statusAdmin=1 AND statusManager=1""")
    annexures = cursor.fetchall()
    return annexures