# internal imports
from dataControllers.cursor import cursor

def removeInLogDB(data):
    """
    This function removes an in log
    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "pooutid": 1,
    }
    """
    cursor.execute(f"DELETE FROM inlog WHERE meterialid = {data['meterialid']} AND goodid = {data['goodid']} AND itemid = {data['itemid']} AND pooutid = {data['pooutid']}")
    return "In log removed successfully"

def removeOutLogDB(data):
    """
    This function removes an out log
    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "workordernumber": 1,
    }
    """
    cursor.execute(f"DELETE FROM outlog WHERE meterialid = {data['meterialid']} AND goodid = {data['goodid']} AND itemid = {data['itemid']} AND workordernumber = {data['workordernumber']}")
    return "Out log removed successfully"

def updateInventoryDB(data):
    """
    This function updates the inventory
    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "pooutid": 1,
    }

    or

    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "workordernumber": 1,
    }
    """

    # firsh check if inlog or outlog
    if "pooutid" in data.keys():

        #this means it is an inlog
        #check if the inventory already has the combination of meterialid, goodid, itemid
        cursor.execute(f"SELECT * FROM inventory WHERE meterialid = {data['meterialid']} AND goodid = {data['goodid']} AND itemid = {data['itemid']}")
        inventory = cursor.fetchall()

        if inventory:
            # then update the quantity and average price
            cursor.execute(f"UPDATE inventory SET quantity = quantity + {data['quantity']} WHERE meterialid = {data['meterialid']} AND goodid = {data['goodid']} AND itemid = {data['itemid']}")
        else:
            # if not, then add the new entry
            cursor.execute(f"INSERT INTO inventory (meterialid, goodid, itemid, quantity) VALUES ({data['meterialid']}, {data['goodid']}, {data['itemid']}, {data['quantity']})")

    else:
        #this means it is an outlog
        #check if the inventory already has the combination of meterialid, goodid, itemid
        cursor.execute(f"SELECT * FROM inventory WHERE meterialid = {data['meterialid']} AND goodid = {data['goodid']} AND itemid = {data['itemid']}")
        inventory = cursor.fetchall()

        if inventory:
            # then update the quantity and average price
            cursor.execute(f"UPDATE inventory SET quantity = quantity - {data['quantity']} WHERE meterialid = {data['meterialid']} AND goodid = {data['goodid']} AND itemid = {data['itemid']}")
        else:
            # if not, then add the new entry
            # return "Inventory does not have the item"
            return "Inventory does not have the item"

    return "Inventory updated successfully"

def addInLogDB(data):
    """
    This function adds an in log
    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "pooutid": 1,
    }
    """
    query = """INSERT INTO inlog ("""
    for key in data.keys():
        query += f"{key}, "

    query = query[:-2] + ") VALUES ("

    for key in data.keys():
        query += f"'{data[key]}', "
    query = query[:-2] + ")"
    cursor.execute(query)
    
    return "In log added successfully"

def addOutLogDB(data):
    """
    This function adds an out log
    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "workordernumber": 1,
    }
    """
    query = """INSERT INTO outlog ("""
    for key in data.keys():
        query += f"{key}, "

    query = query[:-2] + ") VALUES ("

    for key in data.keys():
        query += f"'{data[key]}', "
    query = query[:-2] + ")"
    cursor.execute(query)
    
    return "Out log added successfully"

def getInventoryoutLogDB(woNumber=None):
    """
    This function returns the inventory log
    if the woNumber is provided, it will return the log of that particular wo
    """
    if woNumber:
        cursor.execute(f"SELECT * FROM outlog WHERE workordernumber = {woNumber}")
    else:
        cursor.execute("SELECT * FROM outlog")
    inventoryLog = cursor.fetchall()
    return inventoryLog

def getInventoryinLogDB(poNumber=None):
    """
    This function returns the inventory log
    if the poNumber is provided, it will return the log of that particular po
    """
    if poNumber:
        cursor.execute(f"SELECT * FROM inlog WHERE pooutid = {poNumber}")
    else:
        cursor.execute("SELECT * FROM inlog")
    inventoryLog = cursor.fetchall()
    return inventoryLog

def getGoodsDB():
    """
    This function returns the goods
    """
    cursor.execute("SELECT * FROM goods")
    goods = cursor.fetchall()
    return goods

def getMaterialsDB():
    """
    This function returns the materials
    """
    cursor.execute("SELECT * FROM meterial")
    materials = cursor.fetchall()
    return materials

def getItemsDB():
    """
    This function returns the items
    """
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return items

def newGoodsDB(data):
    """
    This function creates a new goods
    {
        "good_name": "goods_name",
        "good_description": "goods_description",
    }
    """
    query = """INSERT INTO goods ("""
    for key in data.keys():
        query += f"{key}, "

    query = query[:-2] + ") VALUES ("

    for key in data.keys():
        query += f"'{data[key]}', "
    query = query[:-2] + ")"
    cursor.execute(query)
    
    return "Goods created successfully"

def newMaterialDB(data):
    """
    This function creates a new material
    {
        "meterial_name": "material_name",
        "meterial_description": "material_description",
    }
    """
    query = """INSERT INTO meterial ("""
    for key in data.keys():
        query += f"{key}, "

    query = query[:-2] + ") VALUES ("

    for key in data.keys():
        query += f"'{data[key]}', "
    query = query[:-2] + ")"
    cursor.execute(query)
    
    return "Material created successfully"

def newItemDB(data):
    """
    This function creates a new item
    {
        "item_name": "item_name",
        "item_description": "item_description",
        "hsncode": "hsncode",
        "unit": "unit",
    }
    """
    query = """INSERT INTO items ("""
    for key in data.keys():
        query += f"{key}, "

    query = query[:-2] + ") VALUES ("

    for key in data.keys():
        query += f"'{data[key]}', "
    query = query[:-2] + ")"
    cursor.execute(query)
    
    return "Item created successfully"

def getInventoryDB():
    """
    This function returns the inventory
    """   
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    return inventory