# S3 Streaming Pipeline Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MODERN LAKEHOUSE PIPELINE                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         YOUR WORKSTATION                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                       VSCode + Git                            │  │
│  │  • GitHub Integration enabled                                │  │
│  │  • All code in version control                               │  │
│  │  • Ready to push/pull changes                                │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                Python Scripts (Local)                         │  │
│  │                                                               │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                 │  │
│  │  │ stream_text      │  │ stream_csv       │                 │  │
│  │  │ files.py         │  │ files.py         │                 │  │
│  │  │                  │  │                  │                 │  │
│  │  │ 5-sec interval   │  │ 10-sec interval  │                 │  │
│  │  └────────┬─────────┘  └────────┬─────────┘                 │  │
│  │           │                     │                            │  │
│  │  ┌────────┴──────────┬──────────┴────────┐                  │  │
│  │  │                   │                   │                  │  │
│  │  │ ┌────────────────────────────────┐   │                  │  │
│  │  │ │ stream_iot_data.py             │   │                  │  │
│  │  │ │                                │   │                  │  │
│  │  │ │ 4 Sensor Devices               │   │                  │  │
│  │  │ │ 15-sec interval                │   │                  │  │
│  │  │ └────────────────────────────────┘   │                  │  │
│  │  │                                      │                  │  │
│  │  └──────────────────────────────────────┘                  │  │
│  │                   │                                         │  │
│  │  ┌────────────────▼──────────────────┐                    │  │
│  │  │ AWS CLI / Boto3 SDK               │                    │  │
│  │  │ (AWS Credentials Configured)      │                    │  │
│  │  └────────────────┬──────────────────┘                    │  │
│  └───────────────────┼──────────────────────────────────────┘  │
│                      │                                            │
└──────────────────────┼────────────────────────────────────────────┘
                       │
                       │ HTTPS/REST API
                       │
        ┌──────────────▼──────────────┐
        │     AWS ACCOUNT             │
        │                            │
        │ ┌────────────────────────┐ │
        │ │  S3 BUCKET             │ │
        │ │  modern-lakehouse-data │ │
        │ │                        │ │
        │ │ Features:              │ │
        │ │ • AES256 Encryption    │ │
        │ │ • Versioning Enabled   │ │
        │ │ • Lifecycle Policies   │ │
        │ │                        │ │
        │ │ ┌────────────────────┐ │ │
        │ │ │ data/              │ │ │
        │ │ │  ├─ text_files/    │ │ │
        │ │ │  │  └─ year/month/ │ │ │
        │ │ │  │      day/*.txt  │ │ │
        │ │ │  │                 │ │ │
        │ │ │  ├─ csv_files/     │ │ │
        │ │ │  │  └─ year/month/ │ │ │
        │ │ │  │      day/*.csv  │ │ │
        │ │ │  │                 │ │ │
        │ │ │  └─ iot_data/      │ │ │
        │ │ │     └─ device_id/  │ │ │
        │ │ │        year/month/ │ │ │
        │ │ │        day/*.jsonl │ │ │
        │ │ │                    │ │ │
        │ │ │ metadata/          │ │ │
        │ │ │  └─partition_      │ │ │
        │ │ │     metadata.json  │ │ │
        │ │ │                    │ │ │
        │ │ │ logs/ (CloudWatch) │ │ │
        │ │ └────────────────────┘ │ │
        │ │                        │ │
        │ └────────────────────────┘ │
        │                            │
        └────────────────────────────┘
```

---

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                     DATA GENERATION                            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Text Files                CSV Files                IoT Data   │
│  ┌──────────────┐         ┌──────────────┐      ┌───────────┐ │
│  │ Generate     │         │ Generate     │      │ Simulate  │ │
│  │ Random Text  │         │ CSV with     │      │ 4 Sensor  │ │
│  │100 lines     │         │ data 100 rows│      │ Devices   │ │
│  │per file      │         │per file      │      │ 10        │ │
│  │              │         │              │      │ readings  │ │
│  └──────┬───────┘         └──────┬───────┘      │ per batch │ │
│         │                        │              └─────┬─────┘ │
│         └────────────────┬───────┴────────────────────┘       │
│                          │                                     │
│                          ▼                                     │
└────────────────────────────────────────────────────────────────┘
                           │
┌────────────────────────────────────────────────────────────────┐
│                     AWS S3 UPLOAD                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  boto3.put_object() ──┐                                       │
│                       ├──> S3 Client                          │
│  with Metadata        │    ├─ bucket_name                    │
│  with Partitions      │    ├─ s3_key (partitioned path)      │
│                       │    ├─ body (file content)            │
│                       └──> ├─ content_type                   │
│                            └─ metadata                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                   S3 BUCKET STRUCTURE                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  year=2026/month=02/day=01/ ← Automatic Date Partitioning   │
│                                                                │
│  text_files/                 CSV/                IoT/         │
│  ├─ document_0_143022.txt   ├─ data_0.csv      └─ sensor_000/│
│  ├─ document_1_143027.txt   └─ data_1.csv        └─ year=2026│
│  └─ document_2_143032.txt                           ├─month=02│
│                                                      └─day=01/ │
│                                                        ├─ reading_...
│                                                        └─ reading_...
│                                                                │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION & METADATA                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  s3_orchestrator.py                                           │
│  ┌─ Verify partition structure                               │
│  ├─ Count objects per partition                              │
│  ├─ Calculate total data size                                │
│  ├─ Generate partition_metadata.json                         │
│  ├─ Create SQL scripts for Athena                            │
│  └─ Log all operations                                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                   QUERY & ANALYSIS (Optional)                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  AWS Athena              AWS Glue              QuickSight      │
│  ┌──────────────┐        ┌──────────┐        ┌────────────┐  │
│  │ SQL Queries  │──────▶ │ ETL      │ ─────▶ │Dashboards │  │
│  │ on S3 Data   │        │Processing│        │Visualize  │  │
│  └──────────────┘        └──────────┘        └────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Partition Structure Tree

```
s3://modern-lakehouse-data/
│
├── data/
│   │
│   ├── text_files/
│   │   ├── year=2026/
│   │   │   ├── month=01/
│   │   │   │   ├── day=01/
│   │   │   │   │   ├── document_0_143022.txt
│   │   │   │   │   ├── document_1_143027.txt
│   │   │   │   │   └── document_2_143032.txt
│   │   │   │   ├── day=02/
│   │   │   │   │   └── document_3_143022.txt
│   │   │   │   └── ...
│   │   │   └── month=02/
│   │   │       └── ...
│   │   │
│   │   ├── year=2027/
│   │   │   └── ...
│   │   │
│   │   └── ... (future years)
│   │
│   ├── csv_files/
│   │   ├── year=2026/
│   │   │   ├── month=01/
│   │   │   │   ├── day=01/
│   │   │   │   │   ├── data_0_143032.csv
│   │   │   │   │   ├── data_1_143042.csv
│   │   │   │   │   └── data_2_143052.csv
│   │   │   │   └── day=02/
│   │   │   │       └── ...
│   │   │   └── ...
│   │   │
│   │   └── ... (future years)
│   │
│   └── iot_data/
│       ├── device_id=sensor_000/
│       │   ├── year=2026/
│       │   │   ├── month=01/
│       │   │   │   ├── day=01/
│       │   │   │   │   ├── readings_143047_a1b2c3d4.jsonl
│       │   │   │   │   ├── readings_143102_e5f6g7h8.jsonl
│       │   │   │   │   └── ...
│       │   │   │   └── day=02/
│       │   │   │       └── ...
│       │   │   └── ...
│       │   └── ...
│       │
│       ├── device_id=sensor_001/
│       │   ├── year=2026/
│       │   │   └── ...
│       │   └── ...
│       │
│       ├── device_id=sensor_002/
│       │   └── ...
│       │
│       └── device_id=sensor_003/
│           └── ...
│
├── metadata/
│   ├── partition_metadata.json
│   └── ... (other metadata files)
│
└── logs/
    ├── s3_orchestrator.log
    └── ... (other log files)
```

---

## Streaming Timeline

```
Timeline: Every 15 seconds (LCM of 5, 10, 15)

00:00 ┤ Text File 0 ──────────────────────────────────────────
      │ CSV File 0  ──────────────────────────────────────────
      │ IoT Batch 0 ──────────────────────────────────────────
      │
00:05 ├─ Text File 1
      │
00:10 ├─ Text File 2
      │  CSV File 1
      │
00:15 ├─ Text File 3
      │  CSV File 2
      │  IoT Batch 1
      │
00:20 ├─ Text File 4
      │  CSV File 3
      │
00:25 ├─ Text File 5
      │
00:30 ├─ Text File 6
      │  CSV File 4
      │  IoT Batch 2
      │
      └─ ... (pattern repeats)

File Generation per Hour:
- Text Files:  (3600 / 5) = 720 files
- CSV Files:   (3600 / 10) = 360 files
- IoT Batches: (3600 / 15) = 240 batches
  - Total IoT files: 240 × 4 devices = 960 files

TOTAL: ~2040 files per hour
```

---

## Infrastructure Components

```
┌─────────────────────────────────────────────────────────────┐
│               WINDOWS LOCAL MACHINE                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  VSCode                                              │ │
│  │  ├─ Python Extension                                 │ │
│  │  ├─ Git Integration                                  │ │
│  │  ├─ Source Control (GitHub)                          │ │
│  │  └─ Terminal (PowerShell)                            │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Python 3.8+                                         │ │
│  │  ├─ boto3==1.28.0                                    │ │
│  │  ├─ botocore==1.31.0                                 │ │
│  │  └─ (other packages)                                 │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  AWS CLI v2                                          │ │
│  │  ├─ Credentials: ~/.aws/credentials                 │ │
│  │  └─ Config: ~/.aws/config                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Git                                                 │ │
│  │  ├─ GitHub integration                              │ │
│  │  ├─ Local repository                                │ │
│  │  └─ Commit history                                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
                           │ HTTPS
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
      ┌──────────────┐            ┌──────────────┐
      │  GitHub                   │  AWS                │
      │  Repository               │  Account             │
      │                           │                      │
      │  - Code                   │  - S3 Bucket         │
      │  - History                │  - CloudWatch        │
      │  - Collaboration          │  - IAM               │
      │                           │  - Logs              │
      └──────────────┘            └──────────────┘
```

---

## Process Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      SETUP PROCESS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Install AWS CLI v2                                          │
│     └─ msiexec.exe /i https://awscli.amazonaws.com/...         │
│        ▼                                                        │
│  2. Install Python Packages                                     │
│     └─ pip install -r requirements_aws.txt                      │
│        ▼                                                        │
│  3. Configure AWS Credentials                                   │
│     └─ aws configure                                            │
│        ├─ Access Key ID                                         │
│        ├─ Secret Access Key                                     │
│        ├─ Region: us-east-1                                     │
│        └─ Format: json                                          │
│           ▼                                                     │
│  4. Configure Git                                               │
│     └─ git config --global user.name "Name"                     │
│        git config --global user.email "email@domain.com"        │
│           ▼                                                     │
│  5. Authorize GitHub in VSCode                                  │
│     └─ Ctrl+Shift+P → "GitHub: Authorize"                       │
│           ▼                                                     │
│  6. Create S3 Bucket                                            │
│     └─ python aws_setup.py                                      │
│        └─ Creates: modern-lakehouse-data                        │
│        └─ With: Encryption, Versioning, Lifecycle               │
│           ▼                                                     │
│  7. Start Streaming (3 terminals)                               │
│     ├─ python stream_text_files.py                              │
│     ├─ python stream_csv_files.py                               │
│     └─ python stream_iot_data.py                                │
│           ▼                                                     │
│  8. Verify & Orchestrate                                        │
│     ├─ aws s3 ls s3://modern-lakehouse-data/ --recursive        │
│     └─ python s3_orchestrator.py                                │
│           ▼                                                     │
│  9. Commit to GitHub                                            │
│     ├─ git add .                                                │
│     ├─ git commit -m "feat: S3 streaming pipeline"              │
│     └─ git push origin main                                     │
│           ▼                                                     │
│  ✅ COMPLETE & READY!                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Last Updated:** February 1, 2026
