include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help up start stop restart status ps clean

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Up all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) up $(c)

up-d: ## Up all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) up -d $(c)

start: ## Start all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) start $(c)

build: ## Build all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) up --build -d $(c)

build-f: ## Build all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) up --build $(c)

stop: ## Stop all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) stop $(c)

restart: ## Restart all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) restart $(c)

rebuild: ## Rebuild all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) bash -c "down && up --build -d"

logs: ## Show logs for all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) logs --tail=$(or $(n), 100) -f $(c)

status: ## Show status of containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) ps

ps: status ## Alias of status

clean: ## Clean all data
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) down

down: clean ## Alias of clean

images: ## Show all images
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) images

exec: ## Exec container
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) bash

manage: ## Get health-check info
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) python manage.py $(e)

health-check: ## Get health-check info
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) python manage.py health_check

shell: ## Exec shell
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) python manage.py shell_plus

test: ## Run tests
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) pytest $(or $(e), .)

cov:
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) pytest --cov=. --cov-config=../.coveragerc --no-cov-on-fail --cov-fail-under=90 $(or $(e), .)

coverage: ## Run tests
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) coverage run --rcfile=../.coveragerc -m pytest $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) coverage report --fail-under=90 -m

perform: ## Perform code by black, isort and autoflake
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) black $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) isort $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) autoflake --in-place --remove-all-unused-imports --recursive $(or $(e), .)

lint: ## Check code by pylint
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), composes/local.yml) exec $(or $(c), api) pylint --load-plugins pylint_django --django-settings-module=settings.default $(or $(e), ../src)

quality: perform lint test health-check