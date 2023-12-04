COMPOSE_FILE = docker-compose.yml

start:
	docker compose -f $(COMPOSE_FILE) up --build

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down --remove-orphans

build:
	docker compose -f $(COMPOSE_FILE) build --no-cache


logs:
	docker compose -f $(COMPOSE_FILE) logs -f

ps:
	docker compose -f $(COMPOSE_FILE) ps

clean:
	docker system prune --volumes --force

rebuild: down build

restart: down start

default: up

# .PHONY: up down build logs exec ps clean reset:db default