
FROM python:3.9.2-alpine3.13

LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>"

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY ./app /app

CMD ["python", "app/main.py"]
