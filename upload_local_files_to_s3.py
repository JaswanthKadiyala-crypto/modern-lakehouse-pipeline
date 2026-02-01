"""
S3 Upload Script - Upload local files to AWS S3
Reads from C:\streaming_data and uploads to S3 bucket
"""

import boto3
import os
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('s3_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BUCKET_NAME = 'modern-lakehouse-data'
LOCAL_DATA_PATH = r'C:\streaming_data'
AWS_REGION = 'us-east-1'

class S3Uploader:
    def __init__(self, bucket_name, region=AWS_REGION):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name=region)
        self.upload_count = 0
        self.error_count = 0
    
    def upload_text_files(self):
        """Upload text files from C:\streaming_data\text_files"""
        text_dir = os.path.join(LOCAL_DATA_PATH, 'text_files')
        
        if not os.path.exists(text_dir):
            logger.error(f"Text directory not found: {text_dir}")
            return
        
        logger.info("=" * 60)
        logger.info("Uploading TEXT FILES to S3")
        logger.info("=" * 60)
        
        now = datetime.now()
        
        for filename in os.listdir(text_dir):
            file_path = os.path.join(text_dir, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            # Create S3 key with date partitioning
            s3_key = (
                f"data/text_files/"
                f"year={now.year}/"
                f"month={now.month:02d}/"
                f"day={now.day:02d}/"
                f"{filename}"
            )
            
            try:
                with open(file_path, 'rb') as f:
                    self.s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        Body=f,
                        ContentType='text/plain',
                        Metadata={'source': 'local_streaming', 'uploaded_at': now.isoformat()}
                    )
                
                logger.info(f"✓ Uploaded: {s3_key}")
                self.upload_count += 1
                
            except Exception as e:
                logger.error(f"✗ Error uploading {filename}: {e}")
                self.error_count += 1
    
    def upload_csv_files(self):
        """Upload CSV files from C:\streaming_data\csv_files"""
        csv_dir = os.path.join(LOCAL_DATA_PATH, 'csv_files')
        
        if not os.path.exists(csv_dir):
            logger.error(f"CSV directory not found: {csv_dir}")
            return
        
        logger.info("=" * 60)
        logger.info("Uploading CSV FILES to S3")
        logger.info("=" * 60)
        
        now = datetime.now()
        
        for filename in os.listdir(csv_dir):
            file_path = os.path.join(csv_dir, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            # Create S3 key with date partitioning
            s3_key = (
                f"data/csv_files/"
                f"year={now.year}/"
                f"month={now.month:02d}/"
                f"day={now.day:02d}/"
                f"{filename}"
            )
            
            try:
                with open(file_path, 'rb') as f:
                    self.s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        Body=f,
                        ContentType='text/csv',
                        Metadata={'source': 'local_streaming', 'uploaded_at': now.isoformat()}
                    )
                
                logger.info(f"✓ Uploaded: {s3_key}")
                self.upload_count += 1
                
            except Exception as e:
                logger.error(f"✗ Error uploading {filename}: {e}")
                self.error_count += 1
    
    def upload_iot_files(self):
        """Upload IoT JSONL files from C:\streaming_data\iot_data"""
        iot_dir = os.path.join(LOCAL_DATA_PATH, 'iot_data')
        
        if not os.path.exists(iot_dir):
            logger.error(f"IoT directory not found: {iot_dir}")
            return
        
        logger.info("=" * 60)
        logger.info("Uploading IoT DATA (JSONL) to S3")
        logger.info("=" * 60)
        
        now = datetime.now()
        
        for filename in os.listdir(iot_dir):
            file_path = os.path.join(iot_dir, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            # Extract device_id from filename (e.g., sensor_001_data.jsonl)
            device_id = filename.split('_data')[0]
            
            # Create S3 key with device and date partitioning
            s3_key = (
                f"data/iot_data/"
                f"device_id={device_id}/"
                f"year={now.year}/"
                f"month={now.month:02d}/"
                f"day={now.day:02d}/"
                f"{filename}"
            )
            
            try:
                with open(file_path, 'rb') as f:
                    self.s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        Body=f,
                        ContentType='application/x-ndjson',
                        Metadata={'source': 'local_streaming', 'device_id': device_id, 'uploaded_at': now.isoformat()}
                    )
                
                logger.info(f"✓ Uploaded: {s3_key}")
                self.upload_count += 1
                
            except Exception as e:
                logger.error(f"✗ Error uploading {filename}: {e}")
                self.error_count += 1
    
    def verify_uploads(self):
        """Verify files were uploaded to S3"""
        logger.info("\n" + "=" * 60)
        logger.info("VERIFYING UPLOADS")
        logger.info("=" * 60)
        
        try:
            # Check text files
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='data/text_files/'
            )
            text_count = response.get('KeyCount', 0)
            logger.info(f"✓ Text files in S3: {text_count}")
            
            # Check CSV files
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='data/csv_files/'
            )
            csv_count = response.get('KeyCount', 0)
            logger.info(f"✓ CSV files in S3: {csv_count}")
            
            # Check IoT files
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='data/iot_data/'
            )
            iot_count = response.get('KeyCount', 0)
            logger.info(f"✓ IoT files in S3: {iot_count}")
            
            logger.info(f"\nTotal objects in S3: {text_count + csv_count + iot_count}")
            
        except Exception as e:
            logger.error(f"Error verifying uploads: {e}")
    
    def print_summary(self):
        """Print upload summary"""
        logger.info("\n" + "=" * 60)
        logger.info("UPLOAD SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Uploaded: {self.upload_count}")
        logger.info(f"Total Errors: {self.error_count}")
        logger.info(f"Bucket: {self.bucket_name}")
        logger.info(f"Log file: s3_upload.log")
        logger.info("=" * 60)

def main():
    """Main upload function"""
    logger.info("Starting S3 Upload Process")
    logger.info(f"Local data path: {LOCAL_DATA_PATH}")
    logger.info(f"S3 bucket: {BUCKET_NAME}")
    
    uploader = S3Uploader(BUCKET_NAME)
    
    # Upload all file types
    uploader.upload_text_files()
    uploader.upload_csv_files()
    uploader.upload_iot_files()
    
    # Verify uploads
    uploader.verify_uploads()
    
    # Print summary
    uploader.print_summary()

if __name__ == '__main__':
    main()
