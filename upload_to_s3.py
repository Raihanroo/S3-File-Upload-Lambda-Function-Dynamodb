
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

# Configuration
bucket_name = os.getenv("S3_BUCKET_NAME")
folder_path = Path(__file__).resolve().parent / "my-assets"

# Create S3 client (uses configured AWS credentials)
s3 = boto3.client("s3")

try:
    s3.head_bucket(Bucket=bucket_name)
except ClientError as exc:
    error_code = exc.response.get("Error", {}).get("Code")
    if error_code in {"404", "NoSuchBucket"}:
        s3.create_bucket(Bucket=bucket_name)
    else:
        raise

# Upload all files in the folder
for file_path in sorted(folder_path.iterdir()):
    if file_path.is_file():
        s3.upload_file(
            str(file_path),
            bucket_name,
            file_path.name,
        )
        print(f"Uploaded: {file_path.name}")

print("All files uploaded successfully!")
