from flask import request, jsonify
import logging

# internal imports
from dataControllers.annexure import createAnnexureDB, fetchAllAnnexuresDB, fetchManagerAnnexuresDB, managerApprovalStatusDB, fetchAdminAnnexuresDB, adminApprovalStatusDB, fetchApprovedAnneuxresDB

def createAnnexure():
    """
    Controller function to create an annexure in the database.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = createAnnexureDB(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error creating annexure: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500



def fetchAllAnneuxres(employeeId, workOrderNumber):
    """
    Controller function to fetch all annexures from the database.
    """
    try:
        allAnnexures = fetchAllAnnexuresDB(employeeId, workOrderNumber)
        return jsonify(allAnnexures), 200

    except Exception as e:
        logging.error(f"Error fetching annexures: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def fetchManagerAnnexures(workOrderNumber):
    """
    Controller function to fetch all annexures for the given workorder number from the annexure table of database.
    """

    try:
        allAnnexures = fetchManagerAnnexuresDB(workOrderNumber)
        return jsonify(allAnnexures), 200
    except Exception as e:
        logging.error(f"Error fetching annexures: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
def managerApprovalStatus():
    """
    Controller function to update the manager's approval status of the annexure in the annexure table of database.

    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = managerApprovalStatusDB(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error updating approval status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    

def fetchAdminAnnexures():
    """
    Controller function to fetch all annexures to be shown the admin from the annexure table of database.
    """
    try:
        allAnnexures = fetchAdminAnnexuresDB()
        return jsonify(allAnnexures), 200

    except Exception as e:
        logging.error(f"Error fetching annexures: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def adminApprovalStatus():
    """
    Controller function to update the admin's approval status of the annexure in the annexure table of database.

    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = adminApprovalStatusDB(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error updating approval status: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
def fetchApprovedAnneuxres():
    """
    Controller function to fetch all approved annexures from the database.
    """
    try:
        allAnnexures = fetchApprovedAnneuxresDB()
        return jsonify(allAnnexures), 200

    except Exception as e:
        logging.error(f"Error fetching annexures: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500