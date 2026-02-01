# Modern Lakehouse Pipeline - S3 Streaming Setup Guide

## 🚀 Quick Start - Step by Step

This guide walks you through setting up streaming data pipelines to AWS S3 with GitHub integration.

---

## **PHASE 1: GitHub Integration in VSCode**

### Step 1.1: Configure Git Locally
Open PowerShell (Administrator) and run:

```powershell
# Set your Git user details
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"

# Enable credential manager
git config --global credential.helper manager-core
```

### Step 1.2: Authenticate GitHub in VSCode
1. Press `Ctrl+Shift+P` in VS Code
2. Search for **"GitHub: Authorize"**
3. Select "Sign in with browser"
4. Complete OAuth flow
5. Return to VS Code (auto-authenticates)

### Step 1.3: Test Git Integration
```powershell
# Verify Git configuration
git config --list

# Check repository status
git status

# View recent commits
git log --oneline -5
```

---

## **PHASE 2: AWS Tools Installation**

### Step 2.1: Install AWS CLI v2
Run in PowerShell (Administrator):

```powershell
# Download and install AWS CLI v2
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify installation
aws --version
```

**Expected output:** `aws-cli/2.13.x...`

### Step 2.2: Install Python AWS Packages
```powershell
# Install AWS SDK and related tools
pip install -r requirements_aws.txt

# Verify installations
python -c "import boto3; print(boto3.__version__)"
```

---

## **PHASE 3: AWS Credentials Configuration**

### Step 3.1: Get AWS Access Keys
1. Go to AWS Console → IAM → Users
2. Click your username
3. Select "Security credentials" tab
4. Click "Create access key"
5. Save Access Key ID and Secret Access Key

### Step 3.2: Configure AWS CLI
```powershell
# Interactive configuration
aws configure

# When prompted, enter:
# AWS Access Key ID: [paste your access key]
# AWS Secret Access Key: [paste your secret key]
# Default region name: us-east-1 (or your region)
# Default output format: json
```

### Step 3.3: Verify Configuration
```powershell
# Test AWS connection
aws s3 ls

# Check configured credentials
aws sts get-caller-identity
```

---

## **PHASE 4: Create S3 Bucket with Partitions**

### Step 4.1: Run Setup Script
```powershell
# Navigate to project directory
cd c:\Users\jkadi\Documents\modern-lakehouse-pipeline

# Run S3 setup script
python aws_setup.py
```

**What this does:**
- ✓ Creates S3 bucket (`modern-lakehouse-data`)
- ✓ Enables versioning
- ✓ Enables encryption (AES256)
- ✓ Sets lifecycle policies
- ✓ Creates partition structure

**Output:**
```
✓ Bucket 'modern-lakehouse-data' created successfully
✓ Versioning enabled on 'modern-lakehouse-data'
✓ Encryption enabled on 'modern-lakehouse-data'
✓ Lifecycle policy configured for 'modern-lakehouse-data'
✓ Created partition: data/text_files/year=2026/month=02/day=01/.keep
✓ Created partition: data/csv_files/year=2026/month=02/day=01/.keep
✓ Created partition: data/iot_data/device_id=device_001/year=2026/month=02/day=01/.keep
```

---

## **PHASE 5: Start Streaming Data**

### Step 5.1: Stream Text Files
Open a new PowerShell terminal:

```powershell
cd c:\Users\jkadi\Documents\modern-lakehouse-pipeline
python stream_text_files.py
```

This streams 5 text files (5-second intervals) to:
```
s3://modern-lakehouse-data/data/text_files/year=2026/month=02/day=01/document_X_HHMMSS.txt
```

### Step 5.2: Stream CSV Files
Open another PowerShell terminal:

```powershell
python stream_csv_files.py
```

This streams 5 CSV files (10-second intervals) to:
```
s3://modern-lakehouse-data/data/csv_files/year=2026/month=02/day=01/data_X_HHMMSS.csv
```

### Step 5.3: Stream IoT Data
Open another PowerShell terminal:

```powershell
python stream_iot_data.py
```

This streams IoT sensor readings (15-second intervals) from 4 devices to:
```
s3://modern-lakehouse-data/data/iot_data/device_id=sensor_001/year=2026/month=02/day=01/readings_HHMMSS_XXXXXXXX.jsonl
```

---

## **PHASE 6: Verify and Orchestrate**

### Step 6.1: Verify Data in S3
```powershell
# List all objects in text_files partition
aws s3 ls s3://modern-lakehouse-data/data/text_files/ --recursive

# List all objects in csv_files partition
aws s3 ls s3://modern-lakehouse-data/data/csv_files/ --recursive

# List all objects in iot_data partition
aws s3 ls s3://modern-lakehouse-data/data/iot_data/ --recursive

# Get bucket statistics
aws s3 ls s3://modern-lakehouse-data/ --summarize --recursive
```

### Step 6.2: Run Orchestrator
```powershell
python s3_orchestrator.py
```

This:
- ✓ Verifies partition structure
- ✓ Creates partition metadata (JSON)
- ✓ Generates SQL scripts for Athena tables
- ✓ Logs results to `s3_orchestrator.log`

---

## **PHASE 7: GitHub Commit and Push**

### Step 7.1: Stage Changes
```powershell
# Stage all files
git add .

# View staged changes
git status
```

### Step 7.2: Create Commit
```powershell
# Commit with meaningful message
git commit -m "feat: Add S3 streaming pipeline with text, CSV, and IoT data"
```

### Step 7.3: Push to GitHub
```powershell
# Push to main branch
git push origin main

# Or push to new feature branch
git push origin -u feature/s3-streaming
```

### Step 7.4: Verify on GitHub
Go to your GitHub repo → Commits → verify the commit is there

---

## **PHASE 8: Continuous Automation (Optional)**

### Option A: Windows Task Scheduler
```powershell
# Create a batch file for continuous streaming
# save as: streaming_jobs.bat

cd c:\Users\jkadi\Documents\modern-lakehouse-pipeline
start python stream_text_files.py
start python stream_csv_files.py
start python stream_iot_data.py
```

Then schedule in Windows Task Scheduler to run every hour.

### Option B: AWS Lambda
Use AWS Lambda for serverless automation with CloudWatch triggers.

---

## **Partition Structure**

Your S3 bucket is organized as:

```
s3://modern-lakehouse-data/
├── data/
│   ├── text_files/
│   │   └── year={YYYY}/month={MM}/day={DD}/
│   │       └── document_{id}_{timestamp}.txt
│   ├── csv_files/
│   │   └── year={YYYY}/month={MM}/day={DD}/
│   │       └── data_{id}_{timestamp}.csv
│   └── iot_data/
│       └── device_id={device_id}/year={YYYY}/month={MM}/day={DD}/
│           └── readings_{timestamp}_{uuid}.jsonl
├── metadata/
│   └── partition_metadata.json
├── logs/
└── (other configurations)
```

---

## **Troubleshooting**

### Issue: "AWS Access Denied"
```powershell
# Verify credentials are correct
aws sts get-caller-identity

# Reconfigure if needed
aws configure
```

### Issue: "Bucket already exists"
The script handles this - it just uses existing bucket.

### Issue: PowerShell execution policy
```powershell
# If scripts won't run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Git authentication fails
```powershell
# Clear credentials and re-authenticate
git credential reject
# Then re-run: git push origin main
```

---

## **Next Steps**

1. ✓ GitHub integration complete
2. ✓ AWS tools installed
3. ✓ S3 bucket created with partitions
4. ✓ Data streaming to S3
5. → Set up AWS Athena for querying (optional)
6. → Configure AWS Glue for ETL (optional)
7. → Set up CloudWatch monitoring (optional)

---

## **Support**

For issues:
1. Check logs: `s3_orchestrator.log`
2. Verify AWS credentials: `aws sts get-caller-identity`
3. Test S3 access: `aws s3 ls`
4. Review CloudWatch logs in AWS Console

---

**Last Updated:** February 1, 2026
