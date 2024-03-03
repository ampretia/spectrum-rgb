FROM python:3.10-buster as builder

RUN pip install --upgrade pip
RUN pip install poetry==1.8.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.11-slim-bullseye as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
WORKDIR /code
COPY ./abridged-cie-cmf.txt /code
COPY ./cie-cmf.txt /code
COPY ./colour_system.py /code
COPY ./main.py /code

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:3000"]