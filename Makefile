# =============================================================================
# Match Prediction App - Makefile
# =============================================================================
# 
# Usage:
#   make help           - Show this help message
#   make setup          - Copy .env.example to .env
#   make build          - Build all Docker images
#   make up             - Start all services (with build if needed)
#   make down           - Stop and remove all containers
#   make restart        - Restart all services
#   make logs           - Show logs from all services
#   make logs-api       - Show logs from App API
#   make logs-ml        - Show logs from ML API
#   make logs-frontend  - Show logs from Frontend
#   make logs-db        - Show logs from PostgreSQL
#   make shell-api       - Get shell in App API container
#   make shell-ml        - Get shell in ML API container
#   make shell-frontend  - Get shell in Frontend container
#   make db-shell       - Get PostgreSQL shell
#   make clean          - Remove containers, volumes, and images
#   make superclean     - Full clean (including node_modules, __pycache__)
#   make test           - Run tests
#   make migrations     - Run database migrations
#   make seed           - Seed the database with initial data
# =============================================================================

.PHONY: help setup build up down restart logs logs-api logs-ml logs-frontend logs-db \
-shell-api shell-ml shell-frontend db-shell clean superclean test migrations seed

# Configuration
DOCKER_COMPOSE = docker compose
EXEC = $(DOCKER_COMPOSE) exec
SERVICE_API = app-api
SERVICE_ML = ml-api
SERVICE_FRONTEND = frontend
SERVICE_DB = postgres

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m

help: ## Show this help message
	@echo "Match Prediction App - Available Commands:"
	@echo ""
	@echo "  General:"
	@echo "    $(GREEN)make setup$(NC)           - Copy .env.example to .env"
	@echo "    $(GREEN)make build$(NC)          - Build all Docker images"
	@echo "    $(GREEN)make up$(NC)             - Start all services"
	@echo "    $(GREEN)make down$(NC)           - Stop and remove containers"
	@echo "    $(GREEN)make restart$(NC)        - Restart all services"
	@echo ""
	@echo "  Logs:"
	@echo "    $(GREEN)make logs$(NC)           - Show logs from all services"
	@echo "    $(GREEN)make logs-api$(NC)       - Show logs from App API"
	@echo "    $(GREEN)make logs-ml$(NC)        - Show logs from ML API"
	@echo "    $(GREEN)make logs-frontend$(NC)  - Show logs from Frontend"
	@echo "    $(GREEN)make logs-db$(NC)        - Show logs from PostgreSQL"
	@echo ""
	@echo "  Shell Access:"
	@echo "    $(GREEN)make shell-api$(NC)       - Get shell in App API container"
	@echo "    $(GREEN)make shell-ml$(NC)        - Get shell in ML API container"
	@echo "    $(GREEN)make shell-frontend$(NC)  - Get shell in Frontend container"
	@echo "    $(GREEN)make db-shell$(NC)        - Get PostgreSQL shell"
	@echo ""
	@echo "  Cleanup:"
	@echo "    $(GREEN)make clean$(NC)          - Remove containers, volumes, images"
	@echo "    $(GREEN)make superclean$(NC)     - Full clean (including dependencies)"
	@echo ""
	@echo "  Development:"
	@echo "    $(GREEN)make test$(NC)           - Run tests"
	@echo "    $(GREEN)make migrations$(NC)     - Run database migrations"
	@echo "    $(GREEN)make seed$(NC)           - Seed the database"
	@echo ""

setup: ## Copy .env.example to .env
	@echo "$(YELLOW)Setting up environment file...$(NC)"
	cp .env.example .env
	@echo "$(GREEN)Done! Please edit .env with your configuration.$(NC)"

build: ## Build all Docker images
	@echo "$(YELLOW)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Build complete!$(NC)"

up: build ## Start all services
	@echo "$(YELLOW)Starting services...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo ""
	@echo "  Frontend: http://localhost:8080"
	@echo "  App API:  http://localhost:8000/docs"
	@echo "  ML API:   http://localhost:8001/docs"
	@echo ""

down: ## Stop and remove containers
	@echo "$(YELLOW)Stopping services...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)Services stopped!$(NC)"

restart: down up ## Restart all services

logs: ## Show logs from all services
	$(DOCKER_COMPOSE) logs -f

logs-api: ## Show logs from App API
	$(DOCKER_COMPOSE) logs -f $(SERVICE_API)

logs-ml: ## Show logs from ML API
	$(DOCKER_COMPOSE) logs -f $(SERVICE_ML)

logs-frontend: ## Show logs from Frontend
	$(DOCKER_COMPOSE) logs -f $(SERVICE_FRONTEND)

logs-db: ## Show logs from PostgreSQL
	$(DOCKER_COMPOSE) logs -f $(SERVICE_DB)

shell-api: ## Get shell in App API container
	$(EXEC) $(SERVICE_API) sh

shell-ml: ## Get shell in ML API container
	$(EXEC) $(SERVICE_ML) sh

shell-frontend: ## Get shell in Frontend container
	$(EXEC) $(SERVICE_FRONTEND) sh

db-shell: ## Get PostgreSQL shell
	$(EXEC) $(SERVICE_DB) psql -U postgres -d footballapp_db

clean: ## Remove containers, volumes, and images
	@echo "$(YELLOW)Cleaning up...$(NC)"
	$(DOCKER_COMPOSE) down -v --rmi local
	@echo "$(GREEN)Cleanup complete!$(NC)"

superclean: clean ## Full clean
	@echo "$(YELLOW)Removing node_modules and Python cache...$(NC)"
	find . -name "node_modules" -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".pytest_cache" -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Superclean complete!$(NC)"

test: ## Run tests
	@echo "$(YELLOW)Running tests...$(NC)"
	$(DOCKER_COMPOSE) run --rm $(SERVICE_API) pytest /app/tests -v
	$(DOCKER_COMPOSE) run --rm $(SERVICE_ML) pytest /app/tests_ml -v
	@echo "$(GREEN)Tests complete!$(NC)"

migrations: ## Run database migrations
	@echo "$(YELLOW)Running migrations...$(NC)"
	@echo "$(YELLOW)Note: Ensure you have Alembic configured for your database.$(NC)"

seed: ## Seed the database
	@echo "$(YELLOW)Seeding database...$(NC)"
	$(EXEC) $(SERVICE_API) python -c "from app.main import lifespan; from app.database import SessionLocal; import asyncio; asyncio.run(lifespan.__aenter__())"
	@echo "$(GREEN)Seeding complete!$(NC)"
