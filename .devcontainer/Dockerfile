FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11-bullseye

ENV PYTHONUNBUFFERED=1

RUN rm -f /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip