# docker build -t gh-trending-api .
# docker run -p 5000:5000 gh-trending-api:latest

FROM python:3.13-slim

LABEL maintainer="Niklas Tiede <niklastiede2@gmail.com>" \
      org.opencontainers.image.title="Github Trending API" \
      org.opencontainers.image.description="API providing data about trending repositories and developers on GitHub" \
      org.opencontainers.image.source="https://github.com/NiklasTiede/Github-Trending-API" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /github-trending-api

COPY ./pyproject.toml ./README.md ./

COPY ./app ./app

RUN pip install --no-cache-dir . && \
    groupadd --system app && \
    useradd --system --gid app --home-dir /github-trending-api app

USER app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '5000') + '/health', timeout=2).read()"

CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port=${PORT:-5000}"]
