import base64
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import argparse

# Description: This script imports Databricks notebooks from a local directory to a specified Databricks workspace path.

# Example: python3 workspace-import.py \
#             --databricks-url https://your.cloud.databricks.com \
#             --databricks-token dapi123456789abcdef123456789abcdef12 \
#             --local-dir ~/Documents/Source/pytest/databricks/notebooks \
#             --workspace-base-path /ops/develop/1.0.0

# inputs
parser = argparse.ArgumentParser(description='Import Databricks notebooks from a local directory to a Databricks workspace.')
parser.add_argument('--databricks-url', required=True, help='Databricks workspace URL (e.g., https://<databricks-instance>.cloud.databricks.com)')
parser.add_argument('--databricks-token', required=True, help='Databricks personal access token for authentication')
parser.add_argument('--local-dir', required=True, help='Local directory containing the notebooks to import')
parser.add_argument('--workspace-base-path', required=True, help='Target directory in the Databricks workspace (e.g., /Users/<username>/notebooks)')
parser.add_argument('--overwrite', action='store_true', default=True, help='Overwrite existing notebooks in the workspace if they already exist')
args = parser.parse_args()

def post_json(url, payload):
    request = Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {args.databricks_token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urlopen(request) as response:
            return response.status, response.read().decode('utf-8')
    except HTTPError as error:
        return error.code, error.read().decode('utf-8')
    except URLError as error:
        return 0, str(error.reason)

# function to import a single notebook to Databricks
# create directory in databricks workspace if it does not exist, by using the local file path to create the corresponding directory structure in the workspace
def import_notebook(local_path, workspace_path):
    # Create the directory structure in the Databricks workspace if it doesn't exist
    workspace_dir = os.path.dirname(workspace_path)
    status_code, response_text = post_json(
        f"{args.databricks_url}/api/2.0/workspace/mkdirs",
        {"path": workspace_dir}
    )
    if status_code != 200:
        print(f"Failed to create directory: {workspace_dir} (Status code: {status_code} Response: {response_text})")
    else:
        print(f"Created directory: {workspace_dir} (Status code: {status_code})")


    
    # Read the notebook content
    with open(local_path, 'r', encoding='utf-8') as f:
        notebook_content = f.read()

    # Encode the notebook content in base64
    encoded_content = base64.b64encode(notebook_content.encode('utf-8')).decode('utf-8')

    # Prepare the API request payload
    payload = {
        "path": workspace_path,
        "language": "PYTHON",  # Change this if your notebooks are in a different language
        "content": encoded_content,
        "overwrite": args.overwrite
    }

    # Make the API request to import the notebook
    status_code, response_text = post_json(
        f"{args.databricks_url}/api/2.0/workspace/import",
        payload
    )

    # Check the response status
    if status_code == 200:
        print(f"Successfully imported: {workspace_path}")
    else:
        print(f"Failed to import: {workspace_path}. Status code: {status_code}, Response: {response_text}")

######################### MAIN ########################
# Iterate through the local directory and import each notebook
for root, dirs, files in os.walk(args.local_dir):
    for file in files:
        if file.endswith('.py') or file.endswith('.ipynb'):  # Adjust the extensions based on your notebook types
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, args.local_dir)
            workspace_file_path = os.path.join(args.workspace_base_path, relative_path).replace("\\", "/")  # Ensure correct path format for Databricks
            
            print(f"")
            print(f"> Importing {local_file_path} to {workspace_file_path}")
            import_notebook(local_file_path, workspace_file_path)
