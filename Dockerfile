# docker build -t gh-trending-api . 
# docker run -p 8000:8000 gh-trending-api:latest

# FROM python:3.9.2-alpine3.13

# LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>"

# WORKDIR /github-trending-api

# COPY ./requirements.txt .

# RUN pip install -r ./requirements.txt

# COPY ./app ./app

# ENTRYPOINT [ "python" ]

# CMD [ "app/main.py" ]


#################### gunicorn added test########

FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

WORKDIR /github-trending-api

# COPY ./requirements.txt .

RUN pip install --no-cache-dir fastapi \
    pip install beautifulsoup4 \
    pip install requests

COPY ./app ./app

ENTRYPOINT [ "python" ]

CMD [ "app/main.py" ]