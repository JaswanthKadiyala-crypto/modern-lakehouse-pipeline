# 🚀 Quick Start Guide (Step-by-Step)

## Prerequisites Check

Before you start, make sure you have:

```bash
# Check Docker is installed
docker --version
# Expected: Docker version 24.0+

# Check Docker Compose is installed
docker-compose --version
# Expected: Docker Compose version 2.20+

# Check Git is installed
git --version
# Expected: git version 2.40+

# Check Python is installed
python --version
# Expected: Python 3.11+
```

---

## Step 1: Clone the Repository

```bash
# Navigate to your documents or projects folder
cd ~/Documents
# or on Windows PowerShell:
cd C:\Users\YourUsername\Documents

# Clone the repository
git clone https://github.com/JaswanthKadiyala-crypto/modern-lakehouse-pipeline.git

# Enter the directory
cd modern-lakehouse-pipeline
```

---

## Step 2: Verify Project Structure

```bash
# List the main folders (should match README)
ls -la
# or on Windows PowerShell:
Get-ChildItem

# You should see:
# ✅ Makefile
# ✅ README.md
# ✅ infra/
# ✅ ingestion/
# ✅ spark_jobs/
# ✅ dbt_snowflake/
# ✅ ml/
# ✅ dags/
# ✅ docs/
```

---

## Step 3: Start Everything!

```bash
# Option 1: Full setup (recommended for first time)
make setup

# This does:
# 1. Starts all Docker services (docker-compose up)
# 2. Creates MinIO buckets
# 3. Generates sample IoT data
# 4. ✅ Ready to go!

# Option 2: Just start services (if you want more control)
make up

# Then separately:
make ingest    # Generate data
```

### What's Happening During Startup?

```
Time 0s:   🐳 Docker services starting...
Time 15s:  ✅ MinIO initialized
Time 30s:  ✅ PostgreSQL ready
Time 45s:  ✅ Airflow Scheduler started
Time 60s:  ✅ Airflow Webserver ready
Time 75s:  ✅ Spark Master & Worker running
Time 90s:  ✅ MLflow started
Time 120s: ✅ ALL SYSTEMS GO!
```

---

## Step 4: Access the Services

Open these URLs in your browser:

### 🎯 Airflow (DAG Orchestration)
```
URL: http://localhost:8080
Username: airflow
Password: airflow
```

**What to do here:**
1. Look for DAG: `lakehouse_end_to_end`
2. Click on it to expand
3. See the DAG structure (not yet scheduled)

### 🪣 MinIO (S3-Compatible Storage)
```
URL: http://localhost:9000
Username: minioadmin
Password: minioadmin
```

**What to do here:**
1. Click "Buckets" in left menu
2. See `lakehouse` bucket created
3. Explore folders:
   - `raw/` - untouched data
   - `bronze/` - standardized
   - `silver/` - cleaned
   - `gold/` - business-ready

### 📊 MLflow (ML Tracking)
```
URL: http://localhost:5000
```

**What to do here:**
1. (Empty now, will populate when ML runs)
2. See experiments, parameters, metrics
3. Compare model performance

### 🔥 Spark Master UI
```
URL: http://localhost:8888
```

**What to do here:**
1. See worker nodes registered
2. View running jobs
3. Check executor logs
4. Monitor memory usage

### 📓 Jupyter Notebook
```
URL: http://localhost:8888/lab
(Note: Different Spark UI is also on 8888, Jupyter will be on different path)
```

**What to do here:**
1. Interactive data exploration
2. Test Spark code before putting in production
3. Create visualizations

---

## Step 5: View the Logs

```bash
# See all logs in real-time
make logs

# This shows:
# - Airflow scheduler decisions
# - Spark job progress
# - MinIO file uploads
# - MLflow tracking
# (Press Ctrl+C to exit)

# View specific service logs:
make logs-airflow      # Airflow only
make logs-spark        # Spark only
make logs-minio        # MinIO only
```

---

## Step 6: Generate Sample Data (if not done in setup)

```bash
# Create fake IoT sensor data and upload to MinIO
make ingest

# What it does:
# 1. Simulates IoT devices: "sensor_001", "sensor_002", etc.
# 2. Each device sends: temperature, humidity, timestamp
# 3. Uploads 100 events to s3://lakehouse/raw/events/
# 4. Uploads batch file: s3://lakehouse/raw/files/devices.csv
```

**Check in MinIO:**
```
1. Go to http://localhost:9000
2. Click bucket: lakehouse
3. Expand folders: raw → events → 2026-01-28 (today's date)
4. See JSON files: sensor_001.json, sensor_002.json, etc.
```

---

## Step 7: Run the Pipeline

```bash
# Trigger the main DAG
make run

# What happens next:
# 1. Airflow DAG run created
# 2. Tasks execute in order:
#    ├─ Task 1: Ingest (read from S3/MinIO)
#    ├─ Task 2: Bronze → Silver (clean)
#    ├─ Task 3: Write Iceberg tables
#    ├─ Task 4: Write Delta tables
#    └─ Task 5: ML training (anomalies + forecast)
# 3. Results written back to S3
```

**Monitor in Airflow UI:**
```
1. Go to http://localhost:8080
2. Find DAG: lakehouse_end_to_end
3. Click → You see the DAG structure
4. Click "Trigger DAG" button
5. Refresh page to see run status
```

---

## Step 8: Check Results

### In MinIO:
```bash
# List files in bronze zone (after processing)
aws s3 ls s3://lakehouse/bronze/ \
  --endpoint-url http://localhost:9000 \
  --recursive
```

### In Airflow:
```bash
# See DAG run completed
# Click on run → see task status
# Click on task → see logs
```

### In MLflow:
```bash
# After ML runs
# Go to http://localhost:5000
# See experiments with metrics
```

---

## 🎓 Learning Checkpoints

After completing above steps, you should understand:

```
✅ Docker Compose orchestrates multiple services
✅ MinIO acts like AWS S3 (stores data)
✅ Airflow schedules and runs DAGs
✅ Spark processes data in parallel
✅ MLflow tracks ML experiments
✅ All connected in one pipeline!
```

---

## Common Commands

```bash
# See all available commands
make help

# Start services
make up

# Stop services
make down

# Stop AND delete all data
make clean

# Watch real-time logs
make logs

# Generate sample data
make ingest

# Trigger the DAG
make run

# Check if services are healthy
make status

# View Airflow-specific logs
make logs-airflow

# View Spark-specific logs
make logs-spark
```

---

## Troubleshooting

### Services won't start?

```bash
# Check Docker is running
docker ps

# If empty, start Docker Desktop or daemon

# Try again
make up
```

### Port already in use?

```bash
# Find what's using port 8080 (example)
lsof -i :8080          # Mac/Linux
netstat -ano | findstr :8080  # Windows

# Kill the process and try again
```

### Containers crash on startup?

```bash
# Check logs for errors
make logs

# View specific service
docker logs lakehouse-airflow-webserver

# Rebuild images (slow but often fixes issues)
make build
```

### Want to reset everything?

```bash
# This DELETES all data
make clean

# Then start fresh
make setup
```

---

## Next Steps

Once you've completed the quick start:

1. **Read Phase 2 Guide** (`docs/phase2_data_ingestion.md`)
   - Understand data generation logic
   - See how data flows to MinIO

2. **Read Phase 3 Guide** (coming soon)
   - Spark transformations
   - Iceberg & Delta tables

3. **Customize the pipeline**
   - Modify data schema
   - Add more sensors
   - Change transformation logic

4. **Deploy to production** (Phase 6)
   - Move to AWS/cloud
   - Use real data sources
   - Add monitoring & alerts

---

## ✅ Quick Start Complete!

You now have a running:

✅ **Data Lake** (MinIO S3)  
✅ **Orchestration** (Airflow)  
✅ **Processing Engine** (Spark)  
✅ **ML Tracking** (MLflow)  
✅ **Interactive Dev** (Jupyter)  

**Next:** Learn Phase 2 - Data Ingestion 📚

---

## 📞 Quick Help

```bash
# Full help
make help

# See what containers are running
docker-compose -f infra/docker-compose.yml ps

# View recent logs
docker-compose -f infra/docker-compose.yml logs --tail=100

# Execute command in container
docker-compose exec airflow-scheduler bash
```

---

**Ready?** Run `make setup` and watch the magic happen! 🚀
