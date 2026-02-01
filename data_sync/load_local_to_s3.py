"""
S3 Loader - Read local files (TEXT, JSON, XML) and load to AWS S3
Supports partitioning by date and file type
"""
import os
import json
import boto3
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('s3_loader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class S3Loader:
    def __init__(self, bucket_name, region='us-east-1'):
        """Initialize S3 client and configuration"""
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.today = datetime.now()
        self.date_prefix = f"year={self.today.year}/month={self.today.month:02d}/day={self.today.day:02d}"
        
        logger.info(f"S3Loader initialized - Bucket: {bucket_name}, Region: {region}")
    
    def load_files(self, local_path, file_types=['*.txt', '*.json', '*.xml']):
        """
        Read local files and upload to S3
        
        Args:
            local_path (str): Path to local directory containing files
            file_types (list): List of file patterns to load (default: .txt, .json, .xml)
        """
        local_dir = Path(local_path)
        
        if not local_dir.exists():
            logger.error(f"Local path does not exist: {local_path}")
            return
        
        logger.info(f"Starting to load files from: {local_path}")
        
        files_loaded = 0
        files_failed = 0
        
        # Find and process files
        for file_pattern in file_types:
            for file_path in local_dir.glob(file_pattern):
                try:
                    self._upload_file(file_path)
                    files_loaded += 1
                except Exception as e:
                    logger.error(f"Failed to upload {file_path}: {str(e)}")
                    files_failed += 1
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Upload Summary:")
        logger.info(f"  Files Loaded: {files_loaded}")
        logger.info(f"  Files Failed: {files_failed}")
        logger.info(f"  Bucket: {self.bucket_name}")
        logger.info(f"  Date Partition: {self.date_prefix}")
        logger.info(f"{'='*60}\n")
    
    def _upload_file(self, file_path):
        """Upload a single file to S3 with proper partitioning"""
        file_path = Path(file_path)
        file_ext = file_path.suffix.lower()
        
        # Determine S3 folder based on file type
        if file_ext == '.txt':
            s3_folder = 'data/text_files'
        elif file_ext == '.json':
            s3_folder = 'data/json_files'
        elif file_ext == '.xml':
            s3_folder = 'data/xml_files'
        else:
            s3_folder = 'data/other_files'
        
        # Build S3 key with partitioning
        s3_key = f"{s3_folder}/{self.date_prefix}/{file_path.name}"
        
        # Read file and upload
        with open(file_path, 'rb') as f:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=f.read(),
                ContentType=self._get_content_type(file_ext)
            )
        
        file_size = file_path.stat().st_size
        logger.info(f"✓ Uploaded {file_path.name} ({file_size} bytes) → s3://{self.bucket_name}/{s3_key}")
    
    def _get_content_type(self, file_ext):
        """Get MIME type based on file extension"""
        mime_types = {
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.xml': 'application/xml'
        }
        return mime_types.get(file_ext, 'application/octet-stream')
    
    def list_uploaded_files(self):
        """List all files uploaded to S3 under data/ prefix"""
        logger.info(f"\nListing all files in s3://{self.bucket_name}/data/")
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='data/'
            )
            
            if 'Contents' not in response:
                logger.info("No files found in S3")
                return
            
            total_size = 0
            for obj in response['Contents']:
                size = obj['Size']
                total_size += size
                logger.info(f"  - {obj['Key']} ({size} bytes)")
            
            logger.info(f"\nTotal files: {len(response['Contents'])}")
            logger.info(f"Total size: {total_size / 1024:.2f} KB\n")
            
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")


def main():
    """Main function"""
    # Configuration
    BUCKET_NAME = 'modern-lakehouse-data'
    AWS_REGION = 'us-east-1'
    LOCAL_DATA_PATH = r'C:\streaming_data'  # Update this path to your local data directory
    
    # Create loader and run
    loader = S3Loader(BUCKET_NAME, AWS_REGION)
    
    # Load files from local directory
    loader.load_files(LOCAL_DATA_PATH, file_types=['*.txt', '*.json', '*.xml'])
    
    # List uploaded files
    loader.list_uploaded_files()


if __name__ == '__main__':
    main()
