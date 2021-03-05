# docker build -t github-trending-api:1.0.0 . 
# docker run -p 8000:8000 github-trending-api:1.0.0

FROM python:3.9.2-alpine3.13

LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>"

WORKDIR /github-trending-api

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY ./app ./app

ENTRYPOINT [ "python" ]

CMD [ "app/main.py" ]
