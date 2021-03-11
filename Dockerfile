# docker build -t gh-trending-api . 
# docker run -p 8000:8000 gh-trending-api:latest

FROM python:3.9.2-alpine3.13

LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>"

WORKDIR /github-trending-api

COPY ./requirements.txt .

RUN apk add --update --no-cache --virtual .build-deps \
    g++ \
    libxml2 \
    libxml2-dev && \
    apk add libxslt-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY ./app ./app

# ENTRYPOINT [ "python" ]

CMD [ "python", "app/main.py" ]
