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
    poetry install --no-dev --no-ansi --no-interaction --no-root

# -------

FROM python:3.9.6-alpine as prd

ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

RUN addgroup -S rssman && adduser -S rssman -G rssman

WORKDIR /app
COPY --from=builder --chown=rssman:rssman /app/.venv /app/.venv
COPY --chown=rssman:rssman . .

ENV PATH="$PATH:/app/.venv/bin"
EXPOSE 6000
CMD ["python", "./app.py"]

