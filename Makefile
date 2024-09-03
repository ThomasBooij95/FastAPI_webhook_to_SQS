# Makefile for Django Commands

# Define the Python interpreter to use (e.g., python3 or python)
PYTHON = python

# Define the default command to run when "make" is executed
.DEFAULT_GOAL := help

# Help message
help:
	@echo "Django Makefile Commands:"
	@echo "  make env                  - Activate the poetry environment"
	@echo "  make rs                   - Start the development server"
	
up:
	docker compose up -d

build:
	docker build -t app ./

start-network:
	docker network create traefik-public

local:
	uvicorn app.main:app --port 0

kill-all:
	docker kill $(docker ps -q)

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

export_requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

ssh:
	ssh ${SSH_URL}