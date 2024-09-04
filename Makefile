# Makefile for Django Commands

# Define the Python interpreter to use (e.g., python3 or python)
PYTHON = python

# Define the default command to run when "make" is executed
.DEFAULT_GOAL := help

# Help message
help:
	@echo "FastAPI Webhook Service Makefile Commands:"
	@echo "  make up                   - Build and run Docker containers"
	@echo "  make start-network        - Create a Traefik public network"
	@echo "  make traefik-up           - Start Traefik using the docker-compose.traefik.yml file"
	@echo "  make service-up           - Build and run the main service Docker containers"
	@echo "  make dev                  - Start the FastAPI development server"
	@echo "  make deploy               - Deploy the application using the deploy.sh script"
	@echo "  make lint                 - Run linting on the project using flake8"
	@echo "  make load_env             - Load environment variables from the .env file"
	@echo "  make export_requirements  - Export Poetry dependencies to requirements.txt"
	@echo "  make ssh                  - SSH into the server specified by the SSH_URL variable"
	
up:
	docker compose up -d --build

start-network:
	docker network create traefik-public

traefik-up:
	docker compose -f docker-compose.traefik.yml up -d

service-up:
	docker compose -f docker-compose.yml up -d --build
dev:
	cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000
deploy:
	./deploy.sh
lint:
	flake8 . 

load_env:
	set -a && source ./app/.env && set +a

export_requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

ssh:
	ssh ${SSH_URL}