FROM python:3.9.6-alpine as builder


ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/

ARG POETRY_VERSION=1.4.0

RUN pip install poetry==${POETRY_VERSION}

# RUN --mount=type=cache,target=/root/.cache/pip pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry config virtualenvs.in-project true && \
    poetry install --no-ansi --no-dev --no-interaction --no-root

# -------

FROM python:3.9.6-alpine as prd

ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 5000
CMD ["python", "./app.py"]

