
from google.cloud import storage
from pdfminer.high_level import extract_text
import io


from google.cloud import storage

def createFolderGCP(data):
    """
    Creates a folder in Google Cloud Storage.
    :param folder_gcp_path: The folder path to be created.
    :return: None
    """
    bucket_name = "zealerp"
    folder_gcp_path = data["folder_gcp_path"]

    # Initialize GCS client and fetch the bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Create a blob with an empty content
    blob = bucket.blob(folder_gcp_path + "/")

    # Upload the empty content to create the folder
    blob.upload_from_string("")

    return {"message": "Folder created successfully."}


def uploadFileGCP(data):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "zealerp"
    # The path to your file to upload
    source_file_name = data['file_content']
    # The ID of your GCS object
    destination_blob_name = data['file_gcp_path']


    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(source_file_name)

    blob.make_public()

    file_url = blob.public_url

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

    return file_url



def getFilesOrFoldersFromPathGCP(path):
    """
    Fetches data inside a given path in the bucket.

    - If the path is a folder:
      - Returns only **direct** files inside that folder with storage links.
      - Returns only **first-level** subfolders (ignores deeper nested folders).
    - If the path is a file:
      - Returns the file path along with its storage link.
    """
    bucket_name = "zealerp"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=path)

    files = []
    folders = set()

    path = path.rstrip("/") + "/" if path else ""

    for blob in blobs:
        new_blob=blob.name
        if path!="":    # for root folder it should not remove the path otherwise it gives error as "empty separator"
            new_blob=blob.name.split(path)[-1]
            print(new_blob)
        if new_blob.__contains__("/"):  # It's a folder
            bob_name_split = new_blob.split("/")
            for i in range(0, len(bob_name_split)-1):
                relative_path = bob_name_split[i]  # Extract first-level folder
                folders.add(path+relative_path)
        elif new_blob!="":
            # Extract only direct files in the given path
            parent_folder = "/".join(blob.name.split("/")[:-1]) + "/"
            if parent_folder == path or path == "":
                files.append({
                    "file_path": path+blob.name[len(path):],
                    "storage_link": blob.public_url
                })

    return {"files": files, "folders": list(folders),"currentPath":path}

from google.cloud import storage

def editFileGCP(data):
    """
    Edits a file in Google Cloud Storage by replacing its content.
    :param data: Dictionary with keys:
        - 'old_file_path': The file path in GCS to be updated.
        - 'new_file_content': The new content to be written to the file.
        - 'new_file_path': The new file path in GCS.
    :return: Public URL of the updated file.
    """
    bucket_name = "zealerp"
    new_file_content = data["new_file_content"]
    old_file_path = data["old_file_gcp_path"]
    new_file_path = data["new_file_gcp_path"]

    deleteFileOrFolderGCP(old_file_path)
    new_file_upload_response=uploadFileGCP({"file_content": new_file_content, "file_gcp_path": new_file_path})


    return {"message": "File edited successfully.", "file_url": new_file_upload_response}

from google.cloud import storage

def deleteFileOrFolderGCP(file_or_folder_gcp_path):
    """
    Deletes a file or all files inside a folder in Google Cloud Storage.
    :param file_or_folder_gcp_path: The file or folder path to be deleted.
    :return: JSON response with a success message.
    """
    bucket_name = "zealerp"

    # Initialize GCS client and fetch the bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = list(bucket.list_blobs(prefix=file_or_folder_gcp_path))

    if not blobs:
        return {"error": f"No such file or folder: {file_or_folder_gcp_path}"}

    # Delete all matching files
    for blob in blobs:
        blob.delete()

    return {"message": f"Deleted {len(blobs)} files/folders under '{file_or_folder_gcp_path}'."}


def downloadFileGCP(file_gcp_path):
    """
    Downloads a file from Google Cloud Storage.
    :param file_gcp_path: The file path in GCS to be downloaded.
    :return: File content as a string.
    """
    bucket_name = "zealerp"

    # Initialize GCS client and fetch the bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_gcp_path)

    # Download the file content
    file_content = blob.download_as_string()

    return file_content


def check_bucket():
    """Check if the bucket exists"""
    bucket_name = "zealerp"
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        return True
    except:
        return False

