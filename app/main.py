import os
from fastapi.security import HTTPBasicCredentials
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from contextlib import asynccontextmanager
from lib.authentication.basic_auth import basic_auth
from lib.encryption import verify_signature
from lib.sqs.read_message_from_sqs import read_messages_from_queue
from lib.sqs.send_message_to_sqs import send_message_to_sqs
from docs.utils import get_description
from fastapi import Depends, FastAPI, Response, Request
from fastapi_cache.backends.redis import RedisBackend
import uvicorn
from dotenv import load_dotenv
from fastapi.openapi.docs import get_swagger_ui_html


app = FastAPI()


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(host="redis", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()


app = FastAPI(
    title="Booij Analytics Webhook Service",
    description=get_description(),
    summary="Booij Analytics Webhook Service. Receives webhooks and posts them to an AQS SQS Queue.",
    version="1.0.1",
    terms_of_service="https://www.booijanalytics.nl/",
    contact={
        "name": "Thomas Booij",
        "url": "https://www.booijanalytics.nl/",
        "email": "thomas@booijanalytics.nl",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=lifespan,
)


@app.get("/")
async def health_check():
    env_variables = dict(os.environ)
    if "AWS_SECRET_ACCESS_KEY" not in env_variables:
        return Response("No AWS secret supplied")
    if "BASIC_AUTH_USERNAME" not in env_variables:
        return Response("No username supplied")
    if "BASIC_AUTH_PASSWORD" not in env_variables:
        return Response("No password supplied")
    return Response("Server is running and healthy!")


@app.post("/webhook")
async def webhook_listener(request: Request) -> Response:
    queue_name = os.getenv("AWS_QUEUE_NAME")
    message_body = str(await request.json())
    signature = request.headers.get("signature")
    payload = await request.body()
    is_valid = verify_signature(payload, signature)
    if not is_valid:
        print(f"Message_body: {message_body}")
        print(f"signature: {signature}")
        print(f"payload: {payload}")
        return Response("Signature not valid, unvalid request.", status_code=401)
    try:
        response = send_message_to_sqs(queue_name, message_body)
    except Exception:
        Response("Internal Server Error, please retry later.", status_code=500)
    return Response(f"AWS Returned: {response}", status_code=200)


@app.head("/webhook")
async def webhook_head() -> Response:
    return Response("You have reached the webhook endpoint.", status_code=200)


@app.get("/read_messages_in_queue")
async def read_messages_in_queue(username: str = Depends(basic_auth)) -> Response:
    queue_name = os.getenv("AWS_QUEUE_NAME")
    messages = read_messages_from_queue(queue_name)
    return Response(
        f"You have reached the read messages endpoint. Messages:{messages}",
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=8001
    )  ## Makes it possible to use the debugger in VS-code.
