from flask import request, jsonify
import logging

# internal imports
from Utils import gcpUpload

def createFolder():
    """
    This function is used to create a folder in the cloud storage.
    :param: folder_gcp_path
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = gcpUpload.createFolderGCP(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error creating folder: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def uploadFile():

    """
    This function is used to upload the file to the cloud storage
    :param: workorder_id,file_content,file_name,file_gcp_path
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = gcpUpload.uploadFileGCP(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error uploading file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def getFilesOrFoldersFromPath():
    """
    This function is used to get the data inside any given path in the bucket. It returns the all the folder's path if present and all the file's path along with their storage link.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = gcpUpload.getFilesOrFoldersFromPathGCP(data['path'])
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error fetching files: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

def editFile():
    """
    This function is used to edit the file in the cloud storage.
    :param: workorder_id,file_content,file_name,file_gcp_path
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        
        # Validate input
        if "old_file_gcp_path" not in data or "new_file_content" not in data:
            raise ValueError("Both 'old_file_path' and 'new_file_content' must be provided.")

        response = gcpUpload.editFileGCP(data)
        return jsonify(response), 201

    except Exception as e:
        logging.error(f"Error editing file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
def deleteFileOrFolder():
    """
    This function is used to delete the file or folder from the cloud storage.
    :param: file_gcp_path
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = gcpUpload.deleteFileOrFolderGCP(data['file_or_folder_gcp_path'])
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error deleting file/folder: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

    
def downloadFile():
    """
    This function is used to download the file from the cloud storage.
    :param: file_gcp_path
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        response = gcpUpload.downloadFileGCP(data)
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error downloading file: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500