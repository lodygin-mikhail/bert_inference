#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = bert_inference
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python
DOCKER_COMPOSE=docker compose

#################################################################################
# COMMANDS                                                                      #
#################################################################################

.PHONY: help start stop restart build logs deps

help:
	@echo "Доступные команды:"
	@echo "  make start     - Запуск всех сервисов"
	@echo "  make stop      - Остановка всех сервисов"
	@echo "  make restart   - Перезапуск сервисов"
	@echo "  make build     - Пересборка образов"
	@echo "  make logs      - Просмотр логов"
	@echo "  make deps      - Обновление requirements.txt"

# Запуск сервисов
start:
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Сервисы запущены"

# Остановка сервисов
stop:
	$(DOCKER_COMPOSE) down
	@echo "✅ Сервисы остановлены"

# Перезапуск
restart: stop start
	@echo "✅ Сервисы перезапущены"

# Пересборка образов
build:
	$(DOCKER_COMPOSE) build --no-cache
	@echo "✅ Образы пересобраны"

# Просмотр логов
logs:
	$(DOCKER_COMPOSE) logs -f airflow-webserver

# Логи шедулера
logs-scheduler:
	$(DOCKER_COMPOSE) logs -f airflow-scheduler

# Обновление requirements.txt
deps:
	uv export --format requirements.txt --no-hashes --no-dev | findstr /v "^-e" > requirements.txt
	@echo "✅ requirements.txt обновлен"
