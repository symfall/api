include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help up start stop restart status ps clean

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Up all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up $(c)

up-d: ## Up all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up -d $(c)

start: ## Start all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) start $(c)

build: ## Build all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build $(c)

build-d: ## Build all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build -d $(c)

stop: ## Stop all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) stop $(c)

restart: ## Restart all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) restart $(c)

rebuild: ## Rebuild all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) bash -c "down && up --build -d"

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
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) bash

manage: ## Get health-check info
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python manage.py $(e)

health-check: ## Get health-check info
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python manage.py health_check

shell: ## Exec shell
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python manage.py shell_plus

test: ## Run tests
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) python manage.py test --keepdb --parallel 4 $(or $(e), .)

coverage: ## Run coverage tests
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) coverage run --rcfile=../.coveragerc manage.py test --keepdb --parallel 4 $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) coverage html
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) coverage report --fail-under=90 -m

perform: ## Perform code by black, isort and autoflake
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) black $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) isort $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), api) autoflake --in-place --remove-all-unused-imports --recursive $(or $(e), .)

lint: ## Check code by darglint and prospector
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec -w /home/user/app $(or $(c), api) darglint -m "{path}:{line} - {msg_id} {msg} {obj}" $(or $(e), src)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec -w /home/user/app $(or $(c), api) prospector $(or $(e), src)

type: ## Check code by pytype
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec -w /home/user/app $(or $(c), api) pytype $(or $(e), src)

quality: health-check perform lint coverage type
