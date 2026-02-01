# ✅ S3 Streaming Setup Checklist

## Pre-Setup Requirements
- [ ] Windows 10/11 or PowerShell 5.1+
- [ ] Python 3.8+ installed
- [ ] GitHub account and repository cloned
- [ ] AWS account with IAM user created
- [ ] Git configured locally

---

## Phase 1: GitHub & VSCode Integration

- [ ] **1.1** Configure Git credentials
  ```powershell
  git config --global user.name "Your Name"
  git config --global user.email "your.email@github.com"
  ```

- [ ] **1.2** Authorize GitHub in VSCode
  - Open VSCode
  - Press `Ctrl+Shift+P`
  - Search "GitHub: Authorize"
  - Complete OAuth flow

- [ ] **1.3** Test Git integration
  ```powershell
  git status
  git log --oneline -5
  ```

---

## Phase 2: AWS CLI Installation

- [ ] **2.1** Install AWS CLI v2
  ```powershell
  msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
  ```

- [ ] **2.2** Verify AWS CLI installation
  ```powershell
  aws --version
  ```

- [ ] **2.3** Install Python AWS packages
  ```powershell
  pip install -r requirements_aws.txt
  ```

- [ ] **2.4** Verify Python packages
  ```powershell
  python -c "import boto3; print(boto3.__version__)"
  ```

---

## Phase 3: AWS Credentials Setup

- [ ] **3.1** Get AWS Access Keys
  - Go to AWS Console → IAM → Users
  - Click your username
  - Select "Security credentials"
  - Click "Create access key"
  - **SAVE** Access Key ID and Secret Access Key

- [ ] **3.2** Configure AWS CLI
  ```powershell
  aws configure
  ```
  When prompted:
  - Access Key ID: [paste your key]
  - Secret Access Key: [paste your secret]
  - Default region: us-east-1
  - Default format: json

- [ ] **3.3** Verify AWS configuration
  ```powershell
  aws sts get-caller-identity
  ```

---

## Phase 4: Create S3 Bucket

- [ ] **4.1** Review AWS setup script
  - Open `aws_setup.py`
  - Review bucket name (default: `modern-lakehouse-data`)
  - Review region (default: `us-east-1`)

- [ ] **4.2** Run AWS setup script
  ```powershell
  python aws_setup.py
  ```

- [ ] **4.3** Verify S3 bucket creation
  ```powershell
  aws s3 ls
  ```

- [ ] **4.4** Verify partition structure
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/ --recursive
  ```

---

## Phase 5: Text File Streaming

- [ ] **5.1** Review text streaming script
  - Open `stream_text_files.py`
  - Check interval: 5 seconds
  - Check batch size: 100 lines

- [ ] **5.2** Open new PowerShell terminal

- [ ] **5.3** Run text streaming
  ```powershell
  python stream_text_files.py
  ```

- [ ] **5.4** Verify text files in S3
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/data/text_files/ --recursive
  ```

---

## Phase 6: CSV File Streaming

- [ ] **6.1** Review CSV streaming script
  - Open `stream_csv_files.py`
  - Check interval: 10 seconds
  - Check batch size: 100 rows

- [ ] **6.2** Open new PowerShell terminal

- [ ] **6.3** Run CSV streaming
  ```powershell
  python stream_csv_files.py
  ```

- [ ] **6.4** Verify CSV files in S3
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/data/csv_files/ --recursive
  ```

---

## Phase 7: IoT Data Streaming

- [ ] **7.1** Review IoT streaming script
  - Open `stream_iot_data.py`
  - Check devices: 4 sensors
  - Check interval: 15 seconds
  - Check batch size: 10 readings per device

- [ ] **7.2** Open new PowerShell terminal

- [ ] **7.3** Run IoT streaming
  ```powershell
  python stream_iot_data.py
  ```

- [ ] **7.4** Verify IoT data in S3
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/data/iot_data/ --recursive
  ```

---

## Phase 8: Orchestration & Verification

- [ ] **8.1** Run orchestrator script
  ```powershell
  python s3_orchestrator.py
  ```

- [ ] **8.2** Verify partition metadata created
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/metadata/
  ```

- [ ] **8.3** Check logs
  - Open `s3_orchestrator.log`
  - Verify no errors

- [ ] **8.4** Get S3 statistics
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/ --summarize --recursive
  ```

---

## Phase 9: GitHub Commit & Push

- [ ] **9.1** Check Git status
  ```powershell
  git status
  ```

- [ ] **9.2** Stage all files
  ```powershell
  git add .
  ```

- [ ] **9.3** Create meaningful commit
  ```powershell
  git commit -m "feat: Add S3 streaming pipeline with text, CSV, and IoT data"
  ```

- [ ] **9.4** Push to GitHub
  ```powershell
  git push origin main
  ```

- [ ] **9.5** Verify on GitHub
  - Go to GitHub repository
  - Check "Commits" section
  - Verify your commit appears

---

## Phase 10: Continuous Monitoring (Optional)

- [ ] **10.1** Set up continuous streaming
  - Keep streaming scripts running in background terminals
  - OR schedule with Windows Task Scheduler
  - OR set up AWS Lambda

- [ ] **10.2** Monitor S3 growth
  ```powershell
  aws s3 ls s3://modern-lakehouse-data/ --summarize --recursive
  ```

- [ ] **10.3** Check CloudWatch logs (optional)
  - Open AWS CloudWatch
  - Review streaming logs

---

## Files to Review

- [ ] `aws_setup.py` - S3 bucket creation
- [ ] `stream_text_files.py` - Text streaming logic
- [ ] `stream_csv_files.py` - CSV streaming logic
- [ ] `stream_iot_data.py` - IoT streaming logic
- [ ] `s3_orchestrator.py` - Orchestration logic
- [ ] `requirements_aws.txt` - Python dependencies
- [ ] `STREAMING_SETUP_GUIDE.md` - Complete guide
- [ ] `QUICK_REFERENCE.md` - Quick reference
- [ ] `SETUP_SUMMARY.md` - Setup summary

---

## Documentation to Read

- [ ] `STREAMING_SETUP_GUIDE.md` - For detailed instructions
- [ ] `QUICK_REFERENCE.md` - For quick start
- [ ] `SETUP_SUMMARY.md` - For overview
- [ ] AWS S3 Documentation: https://docs.aws.amazon.com/s3/
- [ ] Boto3 Documentation: https://boto3.amazonaws.com/

---

## Troubleshooting Checklist

If you encounter issues:

- [ ] **AWS Error: Access Denied**
  ```powershell
  aws sts get-caller-identity
  aws configure
  ```

- [ ] **Git Error: Permission Denied**
  ```powershell
  git config --global user.email "your@email.com"
  git credential reject
  ```

- [ ] **Python Error: ModuleNotFoundError**
  ```powershell
  pip install --upgrade boto3 botocore
  ```

- [ ] **PowerShell: ExecutionPolicy**
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- [ ] **S3: Bucket Already Exists**
  - Script handles this automatically
  - Uses existing bucket

---

## Success Criteria

✅ **Setup is complete when:**

1. GitHub is integrated with VSCode
2. AWS CLI is installed and configured
3. S3 bucket created with partitions
4. Text files streaming to S3
5. CSV files streaming to S3
6. IoT data streaming to S3
7. Orchestrator running successfully
8. All files committed to GitHub
9. No errors in logs
10. S3 bucket contains data

---

## Performance Metrics

After setup, you should see:

- **Text files**: 1 file every 5 seconds
- **CSV files**: 1 file every 10 seconds
- **IoT batches**: 1 batch (4 devices) every 15 seconds
- **Total data**: Growing ~200+ files per hour
- **S3 size**: ~5-10 MB per hour (depends on file sizes)

---

## Estimated Time

- **Complete Setup**: 30-45 minutes
- **Each Phase**: 5-10 minutes
- **Troubleshooting**: Variable

---

## Support Resources

1. **AWS CLI Help**
   ```powershell
   aws help
   aws s3 help
   ```

2. **Boto3 Documentation**
   - https://boto3.amazonaws.com/

3. **GitHub Help**
   - https://docs.github.com/

4. **VSCode Git Guide**
   - https://code.visualstudio.com/docs/sourcecontrol/overview

---

**Created:** February 1, 2026
**Last Updated:** February 1, 2026
**Status:** ✅ Ready to Use
