# 🏗️ Modern Lakehouse Pipeline

End-to-end data engineering project demonstrating modern data stack: Streaming + Batch ingestion → Iceberg/Delta tables on S3 → Snowflake analytics + dbt transformations → ML models with MLflow, all orchestrated by Airflow.

## 🎯 Project Overview

This project showcases a production-ready data lakehouse architecture combining:
- **Data Lake Formats**: Apache Iceberg & Delta Lake
- **Processing**: Apache Spark
- **Warehouse**: Snowflake
- **Transformation**: dbt (data build tool)
- **ML**: Scikit-learn, LightGBM with MLflow tracking
- **Orchestration**: Apache Airflow
- **Storage**: MinIO (S3-compatible) for local development

## 🏛️ Architecture

```
Data Sources → Ingestion → S3/MinIO → Spark Processing
                                           ↓
                                    ┌──────┴──────┐
                                    ↓             ↓
                              Iceberg Tables  Delta Tables
                                    ↓             ↓
                              Snowflake      ML Pipeline
                                    ↓             ↓
                              dbt Marts    Predictions
                                    └──────┬──────┘
                                           ↓
                                   Airflow Orchestration
```

## 🚀 Quick Start

Coming soon! This project is under active development.

## 📚 Tech Stack

- **Languages**: Python 3.11, SQL
- **Processing**: Apache Spark 3.5
- **Table Formats**: Apache Iceberg, Delta Lake
- **Warehouse**: Snowflake
- **Analytics**: dbt Core
- **ML**: Scikit-learn, LightGBM, MLflow
- **Orchestration**: Apache Airflow 2.8
- **Storage**: MinIO (S3-compatible)
- **Infrastructure**: Docker Compose

## 📁 Project Structure

Coming soon!

## 🎓 Learning Objectives

This project demonstrates:
1. Modern lakehouse architecture patterns
2. Multi-format table management (Iceberg + Delta)
3. ELT pipelines with dbt
4. ML model training and tracking
5. Production orchestration with Airflow
6. Infrastructure as Code

## 👤 Author

**Jaswanth Kadiyala**
- GitHub: [@JaswanthKadiyala-crypto](https://github.com/JaswanthKadiyala-crypto)

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes!