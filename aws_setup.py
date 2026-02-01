"""
AWS S3 Configuration and Setup Script
Creates S3 bucket with partitioned structure for text, CSV, and IoT data
"""

import boto3
import json
from datetime import datetime

s3_client = boto3.client('s3')

# Configuration
BUCKET_NAME = 'modern-lakehouse-data'
REGION = 'us-east-1'
PARTITIONS = {
    'text_files': 'data/text_files/year={year}/month={month}/day={day}/',
    'csv_files': 'data/csv_files/year={year}/month={month}/day={day}/',
    'iot_data': 'data/iot_data/device_id={device_id}/year={year}/month={month}/day={day}/',
}

def create_s3_bucket(bucket_name: str, region: str):
    """Create S3 bucket with proper configuration"""
    try:
        if region == 'us-east-1':
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"✓ Bucket '{bucket_name}' created successfully")
        return True
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"✓ Bucket '{bucket_name}' already exists")
        return True
    except Exception as e:
        print(f"✗ Error creating bucket: {e}")
        return False

def enable_versioning(bucket_name: str):
    """Enable versioning on the bucket"""
    try:
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print(f"✓ Versioning enabled on '{bucket_name}'")
    except Exception as e:
        print(f"✗ Error enabling versioning: {e}")

def enable_lifecycle_policy(bucket_name: str):
    """Set up lifecycle policy for data retention"""
    lifecycle_policy = {
        'Rules': [
            {
                'Id': 'archive-old-data',
                'Status': 'Enabled',
                'Prefix': 'data/',
                'Transitions': [
                    {
                        'Days': 30,
                        'StorageClass': 'STANDARD_IA'
                    },
                    {
                        'Days': 90,
                        'StorageClass': 'GLACIER'
                    }
                ],
                'Expiration': {
                    'Days': 2555  # 7 years
                }
            }
        ]
    }
    
    try:
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )
        print(f"✓ Lifecycle policy configured for '{bucket_name}'")
    except Exception as e:
        print(f"✗ Error setting lifecycle policy: {e}")

def enable_encryption(bucket_name: str):
    """Enable server-side encryption"""
    try:
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }
                ]
            }
        )
        print(f"✓ Encryption enabled on '{bucket_name}'")
    except Exception as e:
        print(f"✗ Error enabling encryption: {e}")

def create_partition_structure(bucket_name: str):
    """Create partition folders in S3"""
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    
    partitions_to_create = [
        f"data/text_files/year={year}/month={month}/day={day}/.keep",
        f"data/csv_files/year={year}/month={month}/day={day}/.keep",
        f"data/iot_data/device_id=device_001/year={year}/month={month}/day={day}/.keep",
        f"data/iot_data/device_id=device_002/year={year}/month={month}/day={day}/.keep",
        f"metadata/.keep",
        f"logs/.keep",
    ]
    
    for partition in partitions_to_create:
        try:
            s3_client.put_object(Bucket=bucket_name, Key=partition, Body=b'')
            print(f"✓ Created partition: {partition}")
        except Exception as e:
            print(f"✗ Error creating partition {partition}: {e}")

def main():
    """Main setup function"""
    print("=" * 60)
    print("AWS S3 Bucket Setup")
    print("=" * 60)
    
    # Create bucket
    if not create_s3_bucket(BUCKET_NAME, REGION):
        return
    
    # Configure bucket
    enable_versioning(BUCKET_NAME)
    enable_encryption(BUCKET_NAME)
    enable_lifecycle_policy(BUCKET_NAME)
    
    # Create partition structure
    create_partition_structure(BUCKET_NAME)
    
    print("\n" + "=" * 60)
    print(f"✓ S3 Bucket '{BUCKET_NAME}' is ready for streaming data!")
    print("=" * 60)

if __name__ == '__main__':
    main()
