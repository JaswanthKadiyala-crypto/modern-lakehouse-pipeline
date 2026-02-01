"""
S3 Data Streaming Orchestrator
Manages partitioning, automation, and data loading to S3
"""

import boto3
import json
import logging
from datetime import datetime
from pathlib import Path
import subprocess
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('s3_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class S3DataOrchestrator:
    def __init__(self, bucket_name: str = 'modern-lakehouse-data'):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.partition_config = self._load_partition_config()
    
    def _load_partition_config(self) -> dict:
        """Load partition configuration"""
        return {
            'text_files': {
                'prefix': 'data/text_files/',
                'partition_keys': ['year', 'month', 'day'],
                'format': 'txt'
            },
            'csv_files': {
                'prefix': 'data/csv_files/',
                'partition_keys': ['year', 'month', 'day'],
                'format': 'csv'
            },
            'iot_data': {
                'prefix': 'data/iot_data/',
                'partition_keys': ['device_id', 'year', 'month', 'day'],
                'format': 'jsonl'
            }
        }
    
    def get_s3_inventory(self, prefix: str) -> list:
        """Get list of all objects in S3 with given prefix"""
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
            
            objects = []
            for page in pages:
                if 'Contents' in page:
                    objects.extend(page['Contents'])
            
            return objects
        except Exception as e:
            logger.error(f"Error getting S3 inventory: {e}")
            return []
    
    def verify_partitions(self) -> dict:
        """Verify partitioning structure"""
        logger.info("Verifying S3 partition structure...")
        report = {}
        
        for data_type, config in self.partition_config.items():
            objects = self.get_s3_inventory(config['prefix'])
            report[data_type] = {
                'total_objects': len(objects),
                'total_size_mb': sum(obj['Size'] for obj in objects) / (1024*1024),
                'objects': [obj['Key'] for obj in objects]
            }
            logger.info(f"{data_type}: {len(objects)} objects, "
                       f"{report[data_type]['total_size_mb']:.2f} MB")
        
        return report
    
    def create_partition_metadata(self, metadata_file: str = 'partition_metadata.json'):
        """Create metadata file for partitions"""
        try:
            report = self.verify_partitions()
            
            metadata = {
                'generated_at': datetime.now().isoformat(),
                'bucket_name': self.bucket_name,
                'partitions': report,
                'config': self.partition_config
            }
            
            # Save locally
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f'metadata/{metadata_file}',
                Body=json.dumps(metadata, indent=2).encode('utf-8'),
                ContentType='application/json'
            )
            
            logger.info(f"✓ Partition metadata created: {metadata_file}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error creating partition metadata: {e}")
            return None
    
    def create_glue_partitions(self):
        """Create AWS Glue partitions (requires Glue and Athena setup)"""
        try:
            glue_client = boto3.client('glue')
            athena_client = boto3.client('athena')
            
            # SQL to create external tables
            sql_queries = {
                'text_files': """
                CREATE EXTERNAL TABLE IF NOT EXISTS text_files (
                    id STRING,
                    content STRING,
                    timestamp STRING
                )
                STORED AS TEXTFILE
                LOCATION 's3://modern-lakehouse-data/data/text_files/'
                TBLPROPERTIES ('has_encrypted_data'='false')
                """,
                'csv_files': """
                CREATE EXTERNAL TABLE IF NOT EXISTS csv_files (
                    id STRING,
                    timestamp STRING,
                    value DOUBLE,
                    category STRING,
                    status STRING
                )
                ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
                LOCATION 's3://modern-lakehouse-data/data/csv_files/'
                TBLPROPERTIES ('has_encrypted_data'='false')
                """,
                'iot_data': """
                CREATE EXTERNAL TABLE IF NOT EXISTS iot_data (
                    device_id STRING,
                    location STRING,
                    sensor_type STRING,
                    timestamp STRING,
                    temperature DOUBLE,
                    humidity DOUBLE,
                    pressure DOUBLE,
                    status STRING,
                    reading_id STRING
                )
                STORED AS JSONL
                LOCATION 's3://modern-lakehouse-data/data/iot_data/'
                TBLPROPERTIES ('has_encrypted_data'='false')
                """
            }
            
            logger.info("✓ Glue partition configuration ready")
            return sql_queries
            
        except Exception as e:
            logger.error(f"Error with Glue partitions: {e}")
            return None
    
    def generate_sql_scripts(self):
        """Generate SQL scripts for creating tables"""
        scripts = self.create_glue_partitions()
        
        if scripts:
            script_file = 'create_athena_tables.sql'
            with open(script_file, 'w') as f:
                for table_name, query in scripts.items():
                    f.write(f"-- {table_name}\n{query}\n\n")
            
            logger.info(f"✓ SQL scripts generated: {script_file}")

def main():
    """Main orchestration function"""
    print("=" * 60)
    print("S3 Data Streaming Orchestrator")
    print("=" * 60)
    
    orchestrator = S3DataOrchestrator()
    
    # Verify partitions
    print("\n1. Verifying S3 Partitions...")
    report = orchestrator.verify_partitions()
    
    # Create metadata
    print("\n2. Creating Partition Metadata...")
    orchestrator.create_partition_metadata()
    
    # Generate SQL scripts
    print("\n3. Generating SQL Scripts...")
    orchestrator.generate_sql_scripts()
    
    print("\n" + "=" * 60)
    print("✓ Orchestration Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
