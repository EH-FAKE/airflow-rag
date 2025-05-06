# Makefile

# Se precisar apontar para um docker-compose.yml específico:
DC = docker-compose -f docker-compose.yml

.PHONY: build airflow-up spark-up down

# Builda todas as imagens definidas no compose
build:
	@echo "🔨 Building all images..."
	$(DC) build --pull

# Sobe Airflow (e postgres, minio) em background
airflow-up:
	@echo "☁️  Starting Airflow stack..."
	$(DC) up -d airflow postgres minio

# Sobe Spark master + worker em background
spark-up:
	@echo "🔥 Starting Spark cluster..."
	$(DC) up -d spark spark-worker-1

# Tira todos os serviços down
down:
	@echo "🛑 Bringing everything down..."
	$(DC) down
