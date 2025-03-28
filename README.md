# serverless_uploader
Cloud run function to upload coverage files to GCS

This is a **Python-based Cloud Run service** that allows uploading an **XML file** with metadata via an HTTP endpoint and stores it in a **Google Cloud Storage (GCS) bucket** following a structured path.

## 🚀 Features
- Accepts **multipart/form-data** uploads.
- Metadata is sent as a **JSON string**.
- Stores files in **Google Cloud Storage (`unmerged-coverage`)** using the format:
gs://unmerged-coverage/project/branchName/buildId/filename.xml

## 🛠️ Prerequisites

Before deploying or running this project, ensure you have:
1. A **Google Cloud Project** with billing enabled.
2. A **Google Cloud Storage (GCS) bucket** named **`unmerged-coverage`**.
3. **Cloud Run enabled** in your GCP project.
4. **Google Cloud SDK (`gcloud`) installed**.
5. **Python 3.8+ installed**.

## 🎯 Testing on Cloud Run
Use curl to test the Cloud Run endpoint:

```sh
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -X POST YOUR_CLOUD_RUN_URL \
  -F "file=@features--backup_cobertura.xml" \
  -F "metadata={\"coverageType\": \"cov\", \"project\": \"CSW Installer\", \"product\": \"TBD\", \"buildId\": \"22.24.8\", \"branchName\": \"release\", \"coverageType\": \"unit test\", \"operatingSystem\": \"10\", \"architecture\": \"Windows\", \"coverageProvider\": \"Bullseye\"}"
```
  
Expected Response
```json
{
    "message": "File uploaded successfully",
    "file_url": "https://storage.googleapis.com/unmerged-coverage/CSW-Installer/release/22.24.8/myfile.xml",
    "gcs_path": "gs://unmerged-coverage/CSW-Installer/release/22.24.8/myfile.xml"
}
```
