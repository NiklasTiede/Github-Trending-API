# docker build -t gh-trending-api .
# docker run -p 5000:5000 gh-trending-api:latest

FROM python:3.13-slim

LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>"

WORKDIR /github-trending-api

COPY ./requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

COPY ./app ./app

CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port=${PORT:-5000}"]
