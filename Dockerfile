FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
 && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.3.0
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" \
 && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "projekat1.main:app", "--host", "0.0.0.0", "--port", "8000"]


# 1. MongoDB (koristi zvanični image, bez Dockerfile-a)
#docker run -d --name mongo -p 27018:27017 -v mongo_data:/data/db mongo:7

# 2. Tvoja aplikacija (koristi tvoj Dockerfile)
#docker run -d --name myapi -p 8000:8000 \
#  --add-host=host.docker.internal:host-gateway \
#  -e MONGO_URI=mongodb://host.docker.internal:27018 \
#  -e DB_NAME=test_db \
#  myapi