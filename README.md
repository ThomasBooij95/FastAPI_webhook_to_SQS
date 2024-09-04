# FastAPI Webhook to AWS SQS Queue Service

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-blue)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-v20.10.16-blue)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-SQS-blue.svg)](https://aws.amazon.com/sqs/)
[![Traefik](https://img.shields.io/badge/Traefik-v2.5.6-blue)](https://traefik.io/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)


## Motivation

Accepting data from a webhook and pushing it to a queue enables handling webhook notifications as a batch-process in ELT tasks. Where a downstream system can empty the queue in regular time intervals instead of having to act on each incoming webhook notification. 

## About

**FastAPI Webhook to AWS SQS Queue Service** is a lightweight FastAPI application designed to listen to incoming webhooks and post the payloads to an AWS SQS Queue. HMAC payload verification is included and Traefik is used as a reverse proxy to manage HTTPS certificates.

## Features

- **Webhook Listener**: Receive and process webhooks securely.
- **AWS SQS Integration**: Post validated payloads directly to an AWS SQS Queue.
- **Traefik Integration**: Automatic HTTPS certificate management and routing via Traefik.
- **Basic Authentication**: Secure endpoints using HTTP Basic Authentication.
- **Deployment on VPS**: Deploy with Docker Compose on a VPS.(I use Hetzner)
- **Local Debugging with VS-code**: Attached launch.json for debugging the FastAPI application locally in VS Code. 

## Getting Started

### Prerequisites

- Docker & Docker Compose installed.
- AWS credentials configured.
- Traefik setup for reverse proxy and HTTPS.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ThomasBooij95/FastAPI_webhook_to_SQS.git
   cd FastAPI_webhook_to_SQS
   ```

2. **Set up environment variables:**

Create a .env file in the ./app directory and configure the following:   

```
SECRET_HMAC_KEY=<your_secret_hmac_key>               # Used to validate webhook requests
AWS_ACCESS_KEY_ID=<your_aws_access_key_id>           # AWS Access Key for SQS
AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>   # AWS Secret Key for SQS
AWS_DEFAULT_REGION=<your_aws_default_region>         # AWS Region for SQS
AWS_QUEUE_NAME=<your_aws_queue_name>                 # Name of the SQS queue
BASIC_AUTH_USERNAME=<your_basic_auth_username>       # Username for Basic Authentication of the service
BASIC_AUTH_PASSWORD=<your_basic_auth_password>       # Password for Basic Authentication of the service
SSH_URL=<your_ssh_url_for_vps>                       # SSH URL used in the Makefile to login to your VPS

```

3. **Build and run the application**

```bash
docker-compose up --build
```


### Usage

1. **Health Check:**

   Access the root endpoint to ensure the server is running:

   ```bash
   curl http://localhost:8001/
   ```


2. **Webhook Endpoint:**

   Post a webhook payload to the `/webhook` endpoint:

   ```bash
   curl -X POST http://localhost:8001/webhook -d '{"key": "value"}' -H "signature: your_signature"
   ```


3. **Read Messages from SQS:**

   Retrieve messages from the configured SQS Queue using basic authentication:

   ```bash
   curl -u <BASIC_AUTH_USERNAME>:<BASIC_AUTH_PASSWORD> http://localhost:8001/read_messages_in_queue
   ```

## Deployment

Pull this repo to your VPS and make the .env file in the ./app directory.

Run ```make start-network``` to start the Traefik Docker network.
Run ```make traefik-up``` to start the Traefik Container.
Run ```make service-up``` to start the FastAPI application.

Use the provided deploy.sh script to deploy the application to your VPS or server once you make changes to your application and want to deploy them to your server. Ensure your SSH_URL is correctly configured in the .env file.

```bash
./deploy.sh
```


## Development

You can either run the docker container locally, or use the poetry environment. After installing depencies with ```poetry install``` and activating the environment with ```poetry poetry shell```,
you can start the dev server either by running ```make dev```, or by using the debugger from VS Code with the supplied launch.json file. 

When adding depencies using ```poetry add```, make sure to export them to the requirements.txt file with ```make export_requirements``` so that the dockerfile will pickup the new requirements.


## Contributions


