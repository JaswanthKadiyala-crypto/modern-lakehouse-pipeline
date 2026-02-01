# 🏗️ Foundation Layer Explained

## What We Just Created (Phase 1 Complete!)

You now have the **infrastructure skeleton** for your modern lakehouse. Let me explain each part:

---

## 1️⃣ README.md - Your Project's Front Door

**What it is:**
- The first thing recruiters see when they visit your GitHub
- Contains architecture diagram, tech stack, quick start
- Explains what the project does and why it matters

**Key sections:**
```
✅ Project title + tagline (what it does)
✅ Architecture diagram (shows system design thinking)
✅ Tech stack table (ATS keyword matching for recruiters)
✅ Project structure (shows code organization)
✅ Quick start (proves it works)
✅ Learning objectives (shows you know the "why")
```

**Why this matters for recruiters:**
- 87% of developers check README before cloning
- You get ~10 seconds to impress
- Good README = Signal you're professional

---

## 2️⃣ Makefile - One-Command Everything

**What it is:**
- A shortcut system to avoid typing long Docker/Git commands
- Uses `make` (available on Mac/Linux/Windows)

**Available commands:**
```bash
make setup         # First time: start services + generate data
make up            # Start all services
make down          # Stop all services
make ingest        # Generate sample IoT data
make run           # Trigger Airflow DAG
make logs          # Watch real-time logs
make clean         # Delete everything (careful!)
```

**Why this matters:**
- One command instead of 10
- Reproducible setup across different machines
- Perfect for interviews: "Just run `make setup`"

---

## 3️⃣ Docker-Compose - The Infrastructure Bible

**What is Docker Compose?**

Think of it like a recipe for your entire system:

```yaml
services:
  postgres:    # Database for Airflow metadata
  minio:       # S3-like storage for your data
  airflow:     # Orchestration engine
  spark:       # Data processing
  mlflow:      # ML tracking
```

Instead of manually installing each tool, one command starts everything:
```bash
docker-compose up -d
```

**The 9 Services We Created:**

### Service 1: PostgreSQL (Port 5432)
**Why:** Airflow needs a database to store:
- DAG runs (when did my pipeline run?)
- Task logs (what happened step by step?)
- Connections (how to connect to S3?)
- Variables (API keys, credentials)

Without PostgreSQL, Airflow loses all state when it restarts (bad for production!)

### Service 2: MinIO (Ports 9000, 9001)
**Why:** S3-compatible storage for your data

```
Your Data Flow:
IoT Sensors → MinIO S3 → Spark → Snowflake
                 ↓
         http://localhost:9000
         (Visual file browser)
```

**How it works:**
```
Raw Data Upload:
  s3://lakehouse/raw/events/2026-01-28/sensor_001.json
  
After Spark Processing:
  s3://lakehouse/silver/iot_events/2026-01-28/
  s3://lakehouse/iceberg/device_metrics/
```

### Service 3: Airflow Scheduler (Background)
**Why:** Watches your DAGs and triggers them on schedule

```
Scheduler Logic:
Every morning @ 2 AM:
  1. Check if "lakehouse_end_to_end" DAG should run
  2. Create a DAG Run
  3. Execute tasks in order
  4. Send alerts if anything fails
```

### Service 4: Airflow Webserver (Port 8080)
**Why:** Beautiful UI to see what's happening

```
What you can do here (http://localhost:8080):
✅ View all DAGs (your pipelines)
✅ Trigger a DAG manually
✅ See real-time task status
✅ View logs for each task
✅ Check past run history
✅ Manage connections & secrets
```

### Service 5: Spark Master (Port 8888)
**Why:** Coordinates distributed data processing

```
How Spark Works:
You submit a job:
  "Process 1 billion rows"
    ↓
Spark Master:
  "Split into 100 tasks"
  "Send to workers"
    ↓
Spark Workers:
  (Process 10 million rows each)
    ↓
Results:
  (Come back to master, then written to storage)
```

**Spark Master UI (http://localhost:8888):**
- See running jobs
- Check resource usage
- View executor logs

### Service 6: Spark Worker
**Why:** Actually processes the data

Multiple workers handle data in parallel:
```
Worker 1: Process rows 1-10 million
Worker 2: Process rows 10-20 million
Worker 3: Process rows 20-30 million
...
(All in parallel = fast!)
```

### Service 7: MLflow (Port 5000)
**Why:** Track ML experiments and models

```
When you train a model:

import mlflow

with mlflow.start_run():
  model = IsolationForest(n_estimators=100)
  model.fit(X_train)
  
  # Log everything
  mlflow.log_param("n_estimators", 100)
  mlflow.log_metric("accuracy", 0.92)
  mlflow.log_model(model, "anomaly_detector")
  
# Later, view all experiments at http://localhost:5000
```

**Why it matters:**
- "Which version of my model performs best?"
- "What hyperparameters did I use?"
- "How did accuracy change over time?"

### Service 8: MinIO Init
**Why:** Automatically creates S3 buckets when MinIO starts

```
Creates these buckets automatically:
lakehouse/
  ├── raw/       (untouched source data)
  ├── bronze/    (raw + standardized)
  ├── silver/    (cleaned, validated)
  ├── gold/      (business-ready)
  └── ml/        (ML features & models)
```

### Service 9: Jupyter Notebook (Port 8888)
**Why:** Interactive development environment

```
Use Jupyter to:
1. Explore data: df.head(), df.describe()
2. Test Spark jobs before putting in Airflow
3. Create data visualizations
4. Run SQL queries interactively
```

---

## 4️⃣ Dockerfiles - Custom Images

### Airflow Dockerfile
**What it does:**
```dockerfile
FROM apache/airflow:2.8-python3.11
# Start with base Apache Airflow image

RUN pip install apache-airflow-providers-apache-spark
# Add ability to run Spark jobs from Airflow

RUN pip install boto3
# Add ability to connect to S3/MinIO
```

**Why custom image?**
- Base Airflow doesn't have Spark or S3 support
- We extend it with what we need

### Spark Dockerfile
**What it does:**
```dockerfile
FROM bitnami/spark:3.5.0
# Start with base Spark image

COPY spark-defaults.conf /opt/spark/conf/
# Add our S3/MinIO configuration

ENV SPARK_PACKAGES="org.apache.iceberg:..."
# Add Iceberg & Delta Lake support
```

---

## 5️⃣ spark-defaults.conf - Spark Configuration

**What this does:**
Tells Spark how to connect to MinIO and use table formats

```conf
# "Hey Spark, when you see s3a://..."
spark.hadoop.fs.s3a.endpoint=http://minio:9000
spark.hadoop.fs.s3a.access.key=minioadmin
spark.hadoop.fs.s3a.secret.key=minioadmin

# "Use Iceberg for analytics tables"
spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkSessionCatalog

# "Use Delta Lake for ML"
spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension
```

**Why this matters:**
- Without this, Spark doesn't know where your data lives
- Without this, Iceberg/Delta won't work

---

## 6️⃣ requirements.txt Files

**What they are:**
Python dependency lists for each component

```txt
# ingestion/requirements.txt
pyspark==3.5.0      (Data processing)
faker==18.13.0      (Generate fake data)
boto3==1.26.165     (S3 connectivity)

# ml/requirements.txt
scikit-learn==1.3.1 (ML algorithms)
mlflow==2.9.1       (Experiment tracking)
lightgbm==4.0.0     (Forecasting model)
```

**Why they matter:**
- "This component needs these Python packages"
- Makes it reproducible (same versions = same behavior)

---

## 🔄 How Everything Connects

```
┌─────────────────┐
│  Your DAG File  │ (dags/lakehouse_end_to_end.py)
│  (tells Airflow │
│   what to do)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Airflow Scheduler      │ (docker service)
│  (triggers at 2 AM)     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Step 1: Ingest Data    │
│  ingestion/generator..  │
│  → MinIO S3             │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Step 2: Spark Process  │
│  spark_jobs/bronze..    │
│  → Read from MinIO      │
│  → Transform            │
│  → Write Iceberg/Delta  │
└────────┬────────────────┘
         │
         ├────────┬────────┐
         │        │        │
         ▼        ▼        ▼
      Iceberg  Delta    Other
         │        │
         ├────────┴────────┐
                  │
                  ▼
         ┌──────────────────┐
         │  ML Pipeline     │
         │  ml/train_*.py   │
         │  → MLflow Track  │
         └──────────────────┘
         
         ▼
    Snowflake
    (Receive data)
    
    ▼
    dbt Transformations
    (Create marts)
    
    ▼
    Dashboards!
```

---

## 🎯 What You Can Do Next

### Phase 2: Data Ingestion
Create `ingestion/generator_streaming.py` to:
1. Generate fake IoT sensor data
2. Upload to MinIO S3
3. Simulate streaming events

### Phase 3: Spark Processing
Create `spark_jobs/bronze_to_silver.py` to:
1. Read raw data from S3
2. Clean it (remove nulls, fix types)
3. Write to Iceberg/Delta tables

### Phase 4: Airflow DAG
Create `dags/lakehouse_end_to_end.py` to:
1. Define task dependencies
2. Schedule everything
3. Handle failures with retries

### Phase 5: ML Pipeline
Create `ml/train_anomaly.py` & `ml/train_forecast.py` to:
1. Train models on Delta data
2. Log metrics to MLflow
3. Save predictions to Snowflake

---

## 🚀 Quick Commands Reference

```bash
# First time setup
cd modern-lakehouse-pipeline
make setup              # Start all services + generate data

# View logs
make logs               # Real-time from all services

# Check services are running
docker ps              # See all running containers

# Access UIs
http://localhost:8080   # Airflow
http://localhost:9000   # MinIO
http://localhost:5000   # MLflow
http://localhost:8888   # Spark Master + Jupyter (different port!)

# Stop everything
make down

# Clean everything (delete data)
make clean
```

---

## 📚 Concepts to Remember

| Concept | What It Does | Why It Matters |
|---------|-------------|---|
| **Docker Compose** | Defines all services in one file | One command starts entire pipeline |
| **MinIO** | Fake S3 on your machine | Learn S3 code locally, no AWS bills |
| **Spark** | Distributed data processing | Handle terabytes of data fast |
| **Airflow** | Orchestration & scheduling | Automate pipelines, handle failures |
| **Iceberg/Delta** | Table formats | ACID transactions + analytics |
| **MLflow** | ML experiment tracking | Version control for models |
| **PostgreSQL** | Metadata database | Airflow remembers DAG history |

---

## ✅ Foundation Layer Status

You now have:

✅ **Infrastructure Code** - docker-compose.yml with 9 services
✅ **Configuration** - spark-defaults.conf, Dockerfiles
✅ **Automation** - Makefile with 15+ commands
✅ **Documentation** - Comprehensive README
✅ **Dependencies** - requirements.txt for each component

**Next: We build the actual pipeline (data generation → processing → ML)**

---

## 📞 Questions to Ask Yourself

1. Why do we need PostgreSQL for Airflow? 
   → *To store pipeline history, connections, variables*

2. Why MinIO instead of real AWS S3?
   → *Cost (free), speed (local), no internet needed*

3. Why both Iceberg AND Delta?
   → *Iceberg for analytics (queries), Delta for ML (versioning)*

4. Why multiple Spark workers?
   → *Parallel processing = faster*

5. Why do we track metrics with MLflow?
   → *Know which model performs best*

---

Ready for Phase 2? Let me know and we'll create the **Data Ingestion Layer**! 🚀
