import os
from flask import Flask, request, redirect, url_for, render_template_string
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient
from azure.storage.fileshare import ShareServiceClient
from datetime import datetime

app = Flask(__name__)

# --- Configuration ---
# 1. Connection String: Ideally, set this in the App Service Configuration (Environment Variables).
#    For simple testing scripts, it's often hardcoded, but Env Var is best practice.
CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Resource Names (Must match user instructions)
BLOB_CONTAINER_NAME = "uploads"
TABLE_NAME = "luckytable"
FILE_SHARE_NAME = "luckyshare"

# --- HTML Template ---
# Simple embedded HTML for the UI
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Project 3: Storage Manager</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
        .success { color: green; }
        .error { color: red; }
        button { padding: 10px 20px; font-size: 1rem; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Azure Storage Manager</h1>
    <p>Select a file to upload to Blob, Table, and File Share.</p>
    
    {% if message %}
        <p class="{{ status }}">{{ message }}</p>
    {% endif %}

    <form method="post" enctype="multipart/form-data">
        <label for="file">Choose file:</label>
        <input type="file" name="file" required>
        <br><br>
        <button type="submit">Upload</button>
    </form>
</body>
</html>
"""

def get_clients():
    if not CONNECT_STR:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")
    
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    table_service_client = TableServiceClient.from_connection_string(CONNECT_STR)
    share_service_client = ShareServiceClient.from_connection_string(CONNECT_STR)
    
    return blob_service_client, table_service_client, share_service_client

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    status = "success"

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            try:
                blob_client, table_client, share_client = get_clients()
                
                # 1. Upload to Blob Storage
                blob_client_instance = blob_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=file.filename)
                # Reset file pointer to beginning before reading
                file.seek(0)
                blob_client_instance.upload_blob(file, overwrite=True)

                # 2. Upload to File Share
                file_client = share_client.get_share_client(FILE_SHARE_NAME).get_file_client(file.filename)
                file.seek(0)
                # content needs to be read as bytes
                file_content = file.read() 
                file_client.upload_file(file_content)

                # 3. Add Metadata to Table Storage
                # PartitionKey: Filename (sanitized or category), RowKey: Timestamp (unique ID)
                table_client_instance = table_client.get_table_client(table_name=TABLE_NAME)
                
                entity = {
                    'PartitionKey': 'uploads',
                    'RowKey': str(datetime.utcnow().timestamp()),
                    'Filename': file.filename,
                    'Size': len(file_content),
                    'UploadTime': str(datetime.utcnow())
                }
                table_client_instance.create_entity(entity=entity)

                message = f"Successfully uploaded '{file.filename}' to Blob, Share, and metadata to Table!"

            except Exception as e:
                message = f"Error: {str(e)}"
                status = "error"
        else:
            message = "No file selected."
            status = "error"

    return render_template_string(HTML_TEMPLATE, message=message, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
