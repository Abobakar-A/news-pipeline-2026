import boto3
import os
import json
from datetime import datetime

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id=os.getenv('MINIO_ROOT_USER'),
        aws_secret_access_key=os.getenv('MINIO_ROOT_PASSWORD')
    )

def save_to_minio(data):
    s3 = get_minio_client()
    bucket_name = "news-raw-data"
    
    try:
        s3.head_bucket(Bucket=bucket_name)
    except:
        s3.create_bucket(Bucket=bucket_name)
    
    file_name = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))
    print(f"✅ [MinIO] تم حفظ الأرشيف: {file_name}")

def read_latest_from_minio():
    s3 = get_minio_client()
    bucket_name = "news-raw-data"
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
        latest_file_key = files[0]['Key']
        file_obj = s3.get_object(Bucket=bucket_name, Key=latest_file_key)
        data = json.loads(file_obj['Body'].read().decode('utf-8'))
        return data.get('articles', [])
    return []