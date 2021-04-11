# docker build -t gh-trending-api .
# docker run -p 5000:5000 gh-trending-api:latest

FROM python:3.9.2-alpine3.13

LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>"

WORKDIR /github-trending-api

COPY ./requirements-prod.txt .

RUN apk add --update --no-cache --virtual .build-deps \
    g++ \
    libxml2 \
    libxml2-dev && \
    apk add libxslt-dev && \
    pip install --no-cache-dir -r requirements-prod.txt && \
    apk del .build-deps

COPY ./app ./app

CMD uvicorn app.main:app --host 0.0.0.0 --port=${PORT:-5000}
