# 🚀 AWS S3 Upload & Git Cleanup Guide

## STEP 5B: Clean Up Git Repository

### Step 5B.1: Check what's being tracked
```powershell
cd c:\Users\jkadi\Documents\modern-lakehouse-pipeline
git status
```

### Step 5B.2: Run cleanup script (Interactive)
```powershell
python cleanup_repo.py
```

This will:
1. ✓ Show untracked files
2. ✓ Ask permission to remove them
3. ✓ Clear Git cache
4. ✓ Re-add files (respecting .gitignore)
5. ✓ Commit cleanup
6. ✓ Push to GitHub

### Step 5B.3: Manual cleanup (if preferred)
```powershell
# Remove all untracked files
git clean -fd

# Remove files from Git cache
git rm -r --cached .

# Re-add everything (respecting .gitignore)
git add .

# Commit
git commit -m "chore: Clean up repo - remove untracked files"

# Push
git push origin main
```

---

## STEP 6: Upload Files to S3

### Step 6.1: Verify AWS credentials
```powershell
aws sts get-caller-identity
```

Expected output:
```
{
    "UserId": "...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/..."
}
```

### Step 6.2: Verify S3 bucket exists
```powershell
aws s3 ls | grep modern-lakehouse-data
```

Expected output:
```
2026-02-01 15:30:45 modern-lakehouse-data
```

### Step 6.3: Run S3 upload script
```powershell
cd c:\Users\jkadi\Documents\modern-lakehouse-pipeline
python upload_local_files_to_s3.py
```

Expected output:
```
2026-02-01 15:45:30 - INFO - Starting S3 Upload Process
2026-02-01 15:45:30 - INFO - Local data path: C:\streaming_data
2026-02-01 15:45:30 - INFO - S3 bucket: modern-lakehouse-data
============================================================
Uploading TEXT FILES to S3
============================================================
✓ Uploaded: data/text_files/year=2026/month=02/day=01/document_1.txt
✓ Uploaded: data/text_files/year=2026/month=02/day=01/document_2.txt
✓ Uploaded: data/text_files/year=2026/month=02/day=01/document_3.txt
✓ Uploaded: data/text_files/year=2026/month=02/day=01/document_4.txt
✓ Uploaded: data/text_files/year=2026/month=02/day=01/document_5.txt
============================================================
Uploading CSV FILES to S3
============================================================
✓ Uploaded: data/csv_files/year=2026/month=02/day=01/data_1.csv
✓ Uploaded: data/csv_files/year=2026/month=02/day=01/data_2.csv
✓ Uploaded: data/csv_files/year=2026/month=02/day=01/data_3.csv
✓ Uploaded: data/csv_files/year=2026/month=02/day=01/data_4.csv
✓ Uploaded: data/csv_files/year=2026/month=02/day=01/data_5.csv
============================================================
Uploading IoT DATA (JSONL) to S3
============================================================
✓ Uploaded: data/iot_data/device_id=sensor_001/year=2026/month=02/day=01/sensor_001_data.jsonl
✓ Uploaded: data/iot_data/device_id=sensor_002/year=2026/month=02/day=01/sensor_002_data.jsonl
✓ Uploaded: data/iot_data/device_id=sensor_003/year=2026/month=02/day=01/sensor_003_data.jsonl
✓ Uploaded: data/iot_data/device_id=sensor_004/year=2026/month=02/day=01/sensor_004_data.jsonl
============================================================
VERIFYING UPLOADS
============================================================
✓ Text files in S3: 5
✓ CSV files in S3: 5
✓ IoT files in S3: 4

Total objects in S3: 14
============================================================
UPLOAD SUMMARY
============================================================
Total Uploaded: 14
Total Errors: 0
Bucket: modern-lakehouse-data
Log file: s3_upload.log
============================================================
```

---

## STEP 7: Verify Uploads in S3

### Step 7.1: Check S3 structure
```powershell
# List all files in S3
aws s3 ls s3://modern-lakehouse-data/ --recursive

# Count files by type
aws s3 ls s3://modern-lakehouse-data/data/text_files/ --recursive | Measure-Object | Select-Object -ExpandProperty Count
aws s3 ls s3://modern-lakehouse-data/data/csv_files/ --recursive | Measure-Object | Select-Object -ExpandProperty Count
aws s3 ls s3://modern-lakehouse-data/data/iot_data/ --recursive | Measure-Object | Select-Object -ExpandProperty Count
```

### Step 7.2: View S3 bucket structure
```powershell
aws s3 ls s3://modern-lakehouse-data/data/ --recursive --summarize
```

Expected structure:
```
s3://modern-lakehouse-data/
├── data/
│   ├── text_files/
│   │   └── year=2026/month=02/day=01/
│   │       ├── document_1.txt
│   │       ├── document_2.txt
│   │       ├── document_3.txt
│   │       ├── document_4.txt
│   │       └── document_5.txt
│   ├── csv_files/
│   │   └── year=2026/month=02/day=01/
│   │       ├── data_1.csv
│   │       ├── data_2.csv
│   │       ├── data_3.csv
│   │       ├── data_4.csv
│   │       └── data_5.csv
│   └── iot_data/
│       ├── device_id=sensor_001/
│       │   └── year=2026/month=02/day=01/
│       │       └── sensor_001_data.jsonl
│       ├── device_id=sensor_002/
│       │   └── year=2026/month=02/day=01/
│       │       └── sensor_002_data.jsonl
│       ├── device_id=sensor_003/
│       │   └── year=2026/month=02/day=01/
│       │       └── sensor_003_data.jsonl
│       └── device_id=sensor_004/
│           └── year=2026/month=02/day=01/
│               └── sensor_004_data.jsonl
```

---

## STEP 8: Delete Local Files (After Verification)

### IMPORTANT: Only delete after verifying S3 upload!

```powershell
# List files before deletion
ls C:\streaming_data\

# Delete local streaming data folder
Remove-Item -Path C:\streaming_data -Recurse -Force

# Verify deletion
ls C:\streaming_data 2>&1  # Should show: Cannot find path
```

---

## 📋 Quick Execution Summary

```powershell
# 1. Verify AWS
aws sts get-caller-identity

# 2. Clean Git repo
python cleanup_repo.py

# 3. Upload to S3
python upload_local_files_to_s3.py

# 4. Verify S3
aws s3 ls s3://modern-lakehouse-data/ --recursive --summarize

# 5. Delete local files
Remove-Item -Path C:\streaming_data -Recurse -Force
```

---

## ✅ Success Checklist

- [ ] AWS credentials verified
- [ ] Git repo cleaned and committed
- [ ] Git repo pushed to GitHub
- [ ] S3 upload script executed successfully
- [ ] All 14 files uploaded to S3 (5 text + 5 CSV + 4 IoT)
- [ ] S3 structure verified with correct partitioning
- [ ] Local files deleted from C:\streaming_data
- [ ] Upload log saved: s3_upload.log

---

**Ready to execute? Run the commands above step by step!** 🚀
