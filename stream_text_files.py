"""
Text File Streaming to S3
Generates and streams text files to S3 with timestamp partitions
"""

import boto3
import io
from datetime import datetime
import time
from pathlib import Path

class TextFileStreamer:
    def __init__(self, bucket_name: str = 'modern-lakehouse-data'):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
    
    def generate_text_data(self, document_id: int, num_lines: int = 100) -> str:
        """Generate sample text content"""
        lines = []
        lines.append(f"Document ID: {document_id}")
        lines.append(f"Generated at: {datetime.now().isoformat()}")
        lines.append("-" * 50)
        
        for i in range(num_lines):
            lines.append(f"Line {i+1}: Sample text content for document streaming.")
        
        return "\n".join(lines)
    
    def stream_text_file(self, document_id: int, num_lines: int = 100):
        """Stream a text file to S3 with partitioning"""
        try:
            # Generate data
            content = self.generate_text_data(document_id, num_lines)
            
            # Create partition path with timestamp
            now = datetime.now()
            s3_key = (
                f"data/text_files/"
                f"year={now.year}/"
                f"month={now.month:02d}/"
                f"day={now.day:02d}/"
                f"document_{document_id}_{now.strftime('%H%M%S')}.txt"
            )
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=content.encode('utf-8'),
                ContentType='text/plain',
                Metadata={
                    'document_id': str(document_id),
                    'generated_at': now.isoformat()
                }
            )
            
            print(f"✓ Streamed text file: {s3_key}")
            return True
            
        except Exception as e:
            print(f"✗ Error streaming text file: {e}")
            return False
    
    def continuous_stream(self, interval_seconds: int = 5, max_documents: int = None):
        """Continuously stream text files to S3"""
        print(f"Starting continuous text file streaming (interval: {interval_seconds}s)...")
        doc_count = 0
        
        try:
            while True:
                self.stream_text_file(doc_count, num_lines=50)
                doc_count += 1
                
                if max_documents and doc_count >= max_documents:
                    print(f"✓ Streamed {doc_count} documents. Stopping.")
                    break
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n✓ Streaming stopped. Total documents streamed: {doc_count}")

def main():
    """Main function"""
    streamer = TextFileStreamer()
    
    # Test: Stream 5 documents with 5-second intervals
    print("=" * 60)
    print("Text File Streaming to S3")
    print("=" * 60)
    streamer.continuous_stream(interval_seconds=5, max_documents=5)

if __name__ == '__main__':
    main()
