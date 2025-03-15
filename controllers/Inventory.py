from flask import request, jsonify

from dataControllers.Inventory import (
                                        getInventoryDB,
                                        newItemDB,
                                        newMaterialDB,
                                        newGoodsDB,
                                        getGoodsDB,
                                        getMaterialsDB,
                                        getItemsDB,
                                        getInventoryinLogDB,
                                        getInventoryoutLogDB,
                                        addInLogDB,
                                        addOutLogDB,
                                        updateInventoryDB,
                                        removeInLogDB,
                                        removeOutLogDB,
                                    )

def addInLog():
    """
    This function adds an in log
    {
        "meterialid":1,
        "goodid":1,
        "itemid":1,
        "quantity": 2,
        "ponumber": 1,
    }
    """
    try:
        data = request.get_json()

        addInLogDB(data)
        
        try:
            updateInventoryDB(data)
        except Exception as e:
            # remove the in log if inventory update fails
            removeInLogDB(data)
            throw (e)
        
        return jsonify({"message": "In log added successfully, Inventory updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

def addOutLog():
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

    try:
        data = request.get_json()
        addOutLogDB(data)

        try:
            updateInventoryDB(data)
        except Exception as e:
            # remove the out log if inventory update fails
            removeOutLogDB(data)
            throw (e)

        return jsonify({"message": "Out log added successfully, Inventory updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

def outLog():
    """
    This function returns the inventory log
    if the woNumber is provided, it will return the log of that particular wo
    """

    try:
        if 'woNumber' in request.args:
            woNumber = request.args.get('woNumber')
            inventoryLog = getInventoryoutLogDB(woNumber)
        else:
            inventoryLog = getInventoryoutLogDB()
        return jsonify({"inventoryLog": inventoryLog})
    except Exception as e:
        return jsonify({"error": str(e)})

def inLog():
    """
    This function returns the inventory log
    if the poNumber is provided, it will return the log of that particular po
    """

    try:
        if 'poNumber' in request.args:
            poNumber = request.args.get('poNumber')
            inventoryLog = getInventoryinLogDB(poNumber)
        else:
            inventoryLog = getInventoryinLogDB()
        return jsonify({"inventoryLog": inventoryLog})
    except Exception as e:
        return jsonify({"error": str(e)})

def getGoods():
    """
    This function returns the goods
    """

    try:
        goods = getGoodsDB()
        return jsonify({"goods": goods})
    except Exception as e:
        return jsonify({"error": str(e)})

def getMaterials():
    """
    This function returns the materials
    """

    try:
        materials = getMaterialsDB()
        return jsonify({"materials": materials})
    except Exception as e:
        return jsonify({"error": str(e)})

def getItems():
    """
    This function returns the items
    """

    try:
        items = getItemsDB()
        return jsonify({"items": items})
    except Exception as e:
        return jsonify({"error": str(e)})

def newGoods():
    """
    This function creates a new goods
    {
        "good_name": "goods_name",
        "good_description": "goods_description",
    }
    """

    try:
        data = request.get_json()
        newGoodsDB(data)
        return jsonify({"message": "Goods created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

def newMaterial():
    """
    This function creates a new material
    {
        "material_name": "material_name",
        "material_description": "material_description",
    }
    """

    try:
        data = request.get_json()
        newMaterialDB(data)
        return jsonify({"message": "Material created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


def newItem():
    """
    This function creates a new item
    {
        "item_name": "item_name",
        "item_description": "item_description",
        "hsncode": "hsncode",
        "unit": "unit",
    }
    """

    try:
        data = request.get_json()
        newItemDB(data)
        return jsonify({"message": "Item created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

def getInventory():
    """
    This function returns the inventory
    """   

    try:
        inventory = getInventoryDB()
        return jsonify({"inventory": inventory})
    except Exception as e:
        return jsonify({"error": str(e)})