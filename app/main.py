import os
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager
from lib.sqs.read_message_from_sqs import read_messages_from_queue
from lib.utils import verify_signature
from lib.sqs.send_message_to_sqs import send_message_to_sqs
from docs.utils import get_description
from fastapi import FastAPI, Response, Request
from fastapi_cache.backends.redis import RedisBackend
import uvicorn
from dotenv import load_dotenv

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
    return Response("Server is running and healthy")


# @app.post("/stresslessdogs/webinargeek/subscriptions/webhook")
@app.post("/webhook")
async def webhook_listener(request: Request) -> Response:
    queue_name = "sd_webinargeek_subscriptions"
    message_body = str(await request.json())
    # payload = request.body()
    # Simulated correct signature (for demonstration purposes, normally this would come from the request headers) # flake8: noqa
    # computed_hash = hmac.new(SECRET_TOKEN.encode(), payload, hashlib.sha256).hexdigest()
    # signature = f"sha256={computed_hash}"
    # signature = (
    # f"sha256=a6353e505082e0614d4f1760c1d25e523ee34141bd2d2e5ef1e4648fc1ed128b"
    # )
    # verify_signature(
    #     payload=request.body(),signature=
    # )
    try:
        response = send_message_to_sqs(queue_name, message_body)
    except Exception:
        Response("Internal Server Error, please retry later.", status_code=500)
    # if response:
    #     print(f"Message sent! Message ID: {response['MessageId']}")
    return Response(f"AWS Returned: {response}", status_code=200)


@app.head("/webhook")
async def webhook_head() -> Response:
    return Response("You have reached the webhook endpoint.", status_code=200)


@app.get("/read_messages_in_queue")
async def read_messages_in_queue() -> Response:
    queue_name = "sd_webinargeek_subscriptions"
    messages = read_messages_from_queue(queue_name)
    return Response(
        f"You have reached the read messages endpoint. Messages:{messages}",
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
