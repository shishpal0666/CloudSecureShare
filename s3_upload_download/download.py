import boto3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

if not BUCKET_NAME:
    raise ValueError("❌ BUCKET_NAME environment variable not set.")

s3_client = boto3.client("s3",
                         aws_access_key_id=AWS_ACCESS_KEY,
                         aws_secret_access_key=AWS_SECRET_KEY)

def download_file(filename):
    try:
        s3_client.download_file(BUCKET_NAME, filename, f'files/{filename}')
        print(f"✅ Downloaded {filename} from S3.")
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
