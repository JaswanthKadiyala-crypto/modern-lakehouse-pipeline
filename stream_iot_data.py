"""
IoT Sensor Data Streaming to S3
Generates and streams IoT sensor data to S3 with device partitioning
"""

import boto3
import json
from datetime import datetime, timedelta
import time
import random
import uuid

class IoTDataStreamer:
    def __init__(self, bucket_name: str = 'modern-lakehouse-data'):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.devices = self._initialize_devices()
    
    def _initialize_devices(self) -> list:
        """Initialize IoT devices with unique IDs"""
        return [
            {'device_id': f'sensor_{i:03d}', 'location': f'Zone_{chr(65+i%4)}', 'type': 'temperature'}
            for i in range(4)
        ]
    
    def generate_sensor_reading(self, device: dict) -> dict:
        """Generate a single sensor reading"""
        now = datetime.now()
        
        reading = {
            'device_id': device['device_id'],
            'location': device['location'],
            'sensor_type': device['type'],
            'timestamp': now.isoformat(),
            'temperature': round(20 + random.gauss(0, 5), 2),
            'humidity': round(50 + random.gauss(0, 10), 2),
            'pressure': round(1013 + random.gauss(0, 5), 2),
            'status': random.choice(['ok', 'warning', 'error']),
            'reading_id': str(uuid.uuid4())
        }
        
        return reading
    
    def stream_iot_batch(self, batch_size: int = 10):
        """Stream a batch of IoT readings to S3"""
        try:
            for device in self.devices:
                readings = []
                now = datetime.now()
                
                # Generate batch of readings
                for _ in range(batch_size):
                    reading = self.generate_sensor_reading(device)
                    readings.append(reading)
                
                # Create partition path
                s3_key = (
                    f"data/iot_data/"
                    f"device_id={device['device_id']}/"
                    f"year={now.year}/"
                    f"month={now.month:02d}/"
                    f"day={now.day:02d}/"
                    f"readings_{now.strftime('%H%M%S')}_{uuid.uuid4().hex[:8]}.jsonl"
                )
                
                # Write JSONL format (one JSON object per line)
                content = "\n".join([json.dumps(reading) for reading in readings])
                
                # Upload to S3
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=content.encode('utf-8'),
                    ContentType='application/x-ndjson',
                    Metadata={
                        'device_id': device['device_id'],
                        'batch_size': str(batch_size),
                        'generated_at': now.isoformat()
                    }
                )
                
                print(f"✓ Streamed IoT batch for {device['device_id']}: {s3_key}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error streaming IoT data: {e}")
            return False
    
    def continuous_stream(self, interval_seconds: int = 15, max_batches: int = None, batch_size: int = 10):
        """Continuously stream IoT data to S3"""
        print(f"Starting continuous IoT data streaming (interval: {interval_seconds}s, batch size: {batch_size})...")
        batch_count = 0
        
        try:
            while True:
                self.stream_iot_batch(batch_size)
                batch_count += 1
                
                if max_batches and batch_count >= max_batches:
                    print(f"✓ Streamed {batch_count} batches. Stopping.")
                    break
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n✓ Streaming stopped. Total batches streamed: {batch_count}")

def main():
    """Main function"""
    streamer = IoTDataStreamer()
    
    # Test: Stream 5 batches with 15-second intervals
    print("=" * 60)
    print("IoT Sensor Data Streaming to S3")
    print("=" * 60)
    streamer.continuous_stream(interval_seconds=15, max_batches=5, batch_size=10)

if __name__ == '__main__':
    main()
