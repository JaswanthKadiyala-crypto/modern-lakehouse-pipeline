.PHONY: help setup up down logs ingest run clean

# Colors for output
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m # No Color

help:
	@echo "$(BLUE)========================================$(NC)"
	@echo "$(BLUE)Modern Lakehouse Pipeline - Makefile$(NC)"
	@echo "$(BLUE)========================================$(NC)"
	@echo ""
	@echo "$(GREEN)Available Commands:$(NC)"
	@echo ""
	@echo "  $(YELLOW)make setup$(NC)        - Initialize infrastructure (Docker Compose, seeds data)"
	@echo "  $(YELLOW)make up$(NC)           - Start all services (Airflow, MinIO, Spark, MLflow)"
	@echo "  $(YELLOW)make down$(NC)         - Stop all services"
	@echo "  $(YELLOW)make logs$(NC)         - View real-time Docker logs"
	@echo "  $(YELLOW)make ingest$(NC)       - Generate and upload sample IoT data"
	@echo "  $(YELLOW)make run$(NC)          - Trigger Airflow DAG (lakehouse_end_to_end)"
	@echo "  $(YELLOW)make clean$(NC)        - Stop services and remove volumes (WARNING: loses data)"
	@echo "  $(YELLOW)make dbt-docs$(NC)     - Generate dbt documentation"
	@echo "  $(YELLOW)make status$(NC)       - Check service health"
	@echo ""
	@echo "$(GREEN)Usage Examples:$(NC)"
	@echo "  make setup          # First time setup"
	@echo "  make up logs        # Start and watch logs"
	@echo "  make ingest run     # Generate data and run pipeline"
	@echo "  make clean          # Cleanup everything"
	@echo ""

# 📋 SETUP: Initialize everything
setup: up ingest
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Airflow UI: http://localhost:8080 (airflow/airflow)"
	@echo "  2. MinIO UI:   http://localhost:9000 (minioadmin/minioadmin)"
	@echo "  3. MLflow UI:  http://localhost:5000"
	@echo "  4. Run 'make run' to trigger the DAG"

# 🚀 UP: Start all services
up:
	@echo "$(BLUE)🚀 Starting Docker services...$(NC)"
	docker-compose -f infra/docker-compose.yml up -d
	@echo "$(GREEN)✅ Services started$(NC)"
	@echo "$(YELLOW)⏳ Waiting 30 seconds for services to initialize...$(NC)"
	@sleep 30
	@echo "$(GREEN)✅ Services ready!$(NC)"

# ⬇️ DOWN: Stop all services
down:
	@echo "$(BLUE)⬇️  Stopping Docker services...$(NC)"
	docker-compose -f infra/docker-compose.yml down
	@echo "$(GREEN)✅ Services stopped$(NC)"

# 📋 LOGS: Watch real-time logs
logs:
	@echo "$(BLUE)📋 Tailing logs (Ctrl+C to exit)...$(NC)"
	docker-compose -f infra/docker-compose.yml logs -f

# 📊 STATUS: Check service health
status:
	@echo "$(BLUE)📊 Checking service health...$(NC)"
	@echo ""
	@echo "$(YELLOW)Airflow:$(NC)"
	@curl -s http://localhost:8080/health || echo "❌ Not responding"
	@echo ""
	@echo "$(YELLOW)MinIO:$(NC)"
	@curl -s http://localhost:9000/minio/health/live || echo "❌ Not responding"
	@echo ""
	@echo "$(YELLOW)MLflow:$(NC)"
	@curl -s http://localhost:5000/api/2.0/mlflow/version || echo "❌ Not responding"
	@echo ""

# 📤 INGEST: Generate sample data
ingest:
	@echo "$(BLUE)📤 Generating sample IoT data...$(NC)"
	python ingestion/generator_streaming.py --records 100 --output s3://lakehouse/raw/events/
	@echo "$(GREEN)✅ Data generated and uploaded to MinIO$(NC)"

# ⏰ RUN: Trigger Airflow DAG
run:
	@echo "$(BLUE)⏰ Triggering Airflow DAG: lakehouse_end_to_end$(NC)"
	curl -X POST \
		-H "Content-Type: application/json" \
		-d '{"conf":{}}' \
		http://localhost:8080/api/v1/dags/lakehouse_end_to_end/dagRuns \
		--user airflow:airflow
	@echo "$(GREEN)✅ DAG triggered!$(NC)"
	@echo "$(YELLOW)Check Airflow UI: http://localhost:8080$(NC)"

# 📚 DBT-DOCS: Generate dbt documentation
dbt-docs:
	@echo "$(BLUE)📚 Generating dbt documentation...$(NC)"
	cd dbt_snowflake && dbt docs generate
	@echo "$(GREEN)✅ Documentation generated$(NC)"

# 🧹 CLEAN: Remove all services and volumes
clean:
	@echo "$(YELLOW)⚠️  WARNING: This will delete all data!$(NC)"
	@echo "$(YELLOW)Ctrl+C to cancel, or wait 5 seconds...$(NC)"
	@sleep 5
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	docker-compose -f infra/docker-compose.yml down -v
	rm -rf data/ notebooks/ .dbt/
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

# 🔧 LOGS-AIRFLOW: Airflow logs only
logs-airflow:
	@echo "$(BLUE)🔧 Airflow logs...$(NC)"
	docker-compose -f infra/docker-compose.yml logs -f airflow-webserver

# 🔧 LOGS-SPARK: Spark logs only
logs-spark:
	@echo "$(BLUE)🔧 Spark logs...$(NC)"
	docker-compose -f infra/docker-compose.yml logs -f spark-master

# 🔧 LOGS-MINIO: MinIO logs only
logs-minio:
	@echo "$(BLUE)🔧 MinIO logs...$(NC)"
	docker-compose -f infra/docker-compose.yml logs -f minio

# 🛠️ BUILD: Build Docker images
build:
	@echo "$(BLUE)🛠️  Building Docker images...$(NC)"
	docker-compose -f infra/docker-compose.yml build
	@echo "$(GREEN)✅ Build complete$(NC)"

# 🧪 TEST: Run tests
test:
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	pytest tests/ -v
	@echo "$(GREEN)✅ Tests complete$(NC)"

# ✨ FORMAT: Format code (Black, isort)
format:
	@echo "$(BLUE)✨ Formatting Python code...$(NC)"
	black . --line-length 100
	isort . --profile black
	@echo "$(GREEN)✅ Formatting complete$(NC)"

# 🔍 LINT: Check code quality
lint:
	@echo "$(BLUE)🔍 Linting code...$(NC)"
	flake8 . --max-line-length=100 --exclude=.git,__pycache__,venv
	@echo "$(GREEN)✅ Lint check complete$(NC)"

# Default target
.DEFAULT_GOAL := help
