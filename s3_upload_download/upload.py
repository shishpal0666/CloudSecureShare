import boto3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()


# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

if not BUCKET_NAME:
    raise ValueError("❌ BUCKET_NAME environment variable not set.")

s3_client = boto3.client("s3",
                         aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY)

def upload_file(file):
    try:
        s3_client.upload_file(file, BUCKET_NAME, os.path.basename(file))
        print(f"✅ Uploaded {file} to S3.")
    except Exception as e:
        print(f"❌ Error uploading {file}: {e}")
