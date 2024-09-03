FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY ./app /app
