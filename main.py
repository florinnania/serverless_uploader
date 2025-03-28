import json
import os
from flask import Request, jsonify
from google.cloud import storage

# GCS Config
BUCKET_NAME = "unmerged-coverage"

# Initialize GCS Client
storage_client = storage.Client()

# Define the function using the functions_framework decorator
import functions_framework

@functions_framework.http
def upload_file(request: Request):
    """Handles file uploads with metadata and stores them in GCS"""
    
    if request.method != "POST":
        return jsonify({"error": "Only POST method is allowed"}), 405
    
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    metadata = request.form.get("metadata")

    if not file or not metadata:
        return jsonify({"error": "Missing file or metadata"}), 400

    try:
        metadata_json = json.loads(metadata)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid metadata JSON"}), 400

    # Extract required metadata fields
    required_fields = ["project", "branchName", "buildId"]
    for field in required_fields:
        if field not in metadata_json:
            return jsonify({"error": f"Missing required metadata field: {field}"}), 400

    # Sanitize project name (replace spaces with hyphens)
    project = metadata_json["project"].replace(" ", "-")
    branch = metadata_json["branchName"]
    build_id = metadata_json["buildId"]

    # Define the folder structure
    destination_blob_name = f"{project}/{branch}/{build_id}/{file.filename}"

    # Upload to GCS
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, content_type="application/xml")

    return jsonify({
        "message": "File uploaded successfully",
        "gcs_path": f"gs://{BUCKET_NAME}/{destination_blob_name}"
    }), 200
