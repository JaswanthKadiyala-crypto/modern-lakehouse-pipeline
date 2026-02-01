# ==============================================================================
# Airflow Docker Image
# ==============================================================================
# This Dockerfile creates an Airflow image with all dependencies
# for running the lakehouse DAGs

FROM apache/airflow:2.8-python3.11

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies for Airflow and data processing
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.8.1 \
    apache-airflow-providers-amazon==8.21.0 \
    boto3==1.26.165 \
    pyspark==3.5.0 \
    pandas==2.0.3 \
    pyarrow==12.0.1 \
    requests==2.31.0 \
    python-dotenv==1.0.0

# Initialize Airflow database
ENV AIRFLOW_HOME=/opt/airflow

# Expose port for Webserver
EXPOSE 8080 8793

# Default command
CMD ["airflow", "webserver"]
