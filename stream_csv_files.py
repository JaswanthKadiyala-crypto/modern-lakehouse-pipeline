"""
CSV File Streaming to S3
Generates and streams CSV files to S3 with timestamp partitions
"""

import boto3
import csv
import io
from datetime import datetime, timedelta
import time
import random

class CSVFileStreamer:
    def __init__(self, bucket_name: str = 'modern-lakehouse-data'):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
    
    def generate_csv_data(self, file_id: int, num_rows: int = 100) -> str:
        """Generate sample CSV content"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['id', 'timestamp', 'value', 'category', 'status'])
        
        # Write data rows
        now = datetime.now()
        for i in range(num_rows):
            timestamp = now - timedelta(seconds=i*60)
            writer.writerow([
                f"row_{file_id}_{i}",
                timestamp.isoformat(),
                round(random.uniform(10, 1000), 2),
                random.choice(['A', 'B', 'C', 'D']),
                random.choice(['active', 'inactive', 'pending'])
            ])
        
        return output.getvalue()
    
    def stream_csv_file(self, file_id: int, num_rows: int = 100):
        """Stream a CSV file to S3 with partitioning"""
        try:
            # Generate data
            content = self.generate_csv_data(file_id, num_rows)
            
            # Create partition path with timestamp
            now = datetime.now()
            s3_key = (
                f"data/csv_files/"
                f"year={now.year}/"
                f"month={now.month:02d}/"
                f"day={now.day:02d}/"
                f"data_{file_id}_{now.strftime('%H%M%S')}.csv"
            )
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=content.encode('utf-8'),
                ContentType='text/csv',
                Metadata={
                    'file_id': str(file_id),
                    'num_rows': str(num_rows),
                    'generated_at': now.isoformat()
                }
            )
            
            print(f"✓ Streamed CSV file: {s3_key} ({num_rows} rows)")
            return True
            
        except Exception as e:
            print(f"✗ Error streaming CSV file: {e}")
            return False
    
    def continuous_stream(self, interval_seconds: int = 10, max_files: int = None):
        """Continuously stream CSV files to S3"""
        print(f"Starting continuous CSV file streaming (interval: {interval_seconds}s)...")
        file_count = 0
        
        try:
            while True:
                self.stream_csv_file(file_count, num_rows=100)
                file_count += 1
                
                if max_files and file_count >= max_files:
                    print(f"✓ Streamed {file_count} CSV files. Stopping.")
                    break
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n✓ Streaming stopped. Total CSV files streamed: {file_count}")

def main():
    """Main function"""
    streamer = CSVFileStreamer()
    
    # Test: Stream 5 CSV files with 10-second intervals
    print("=" * 60)
    print("CSV File Streaming to S3")
    print("=" * 60)
    streamer.continuous_stream(interval_seconds=10, max_files=5)

if __name__ == '__main__':
    main()
