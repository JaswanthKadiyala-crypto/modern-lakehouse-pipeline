# ==============================================================================
# Spark Docker Image
# ==============================================================================
# This Dockerfile creates a Spark image with Iceberg and Delta Lake support

FROM bitnami/spark:3.5.0

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Spark packages for:
# - Iceberg: columnar table format for big data
# - Delta Lake: ACID transactions for data lakes
# - S3/MinIO support: object storage connectivity
# - Hadoop: distributed storage framework
ENV SPARK_PACKAGES="org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.4.0,\
io.delta:delta-spark_2.12:3.0.0,\
org.apache.hadoop:hadoop-aws:3.3.4,\
com.amazonaws:aws-java-sdk-bundle:1.12.565,\
org.apache.hadoop:hadoop-common:3.3.4"

# Copy Spark configuration for S3/MinIO
COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

USER 1001

EXPOSE 7077 8080 8081

CMD ["spark-class", "org.apache.spark.deploy.master.Master"]
