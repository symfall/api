include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help up start stop restart status ps clean

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up $(c)

start: ## Start all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up -d $(c)

build: ## Build all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build -d $(c)

build-f: ## Build all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build -d $(c)

stop: ## Stop all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) stop $(c)

restart: ## Restart all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) restart $(c)

rebuild: ## Rebuild all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) down
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build -d

logs: ## Show logs for all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) logs --tail=$(or $(n), 100) -f $(c)

status: ## Show status of containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) ps

ps: status ## Alias of status

clean: ## Clean all data
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) down

down: clean ## Alias of clean

images: ## Show all images
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) images

exec: ## Exec container
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) poetry install
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) bash

shell: ## Exec shell
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python src/manage.py shell_plus

run-command: ## Run command in shell
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python -c="$(e)"

manage:
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python src/manage.py $(e)
