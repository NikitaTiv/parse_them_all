FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tesseract_api
COPY Pipfile Pipfile.lock ./

RUN pip install pipenv==2025.0.3
RUN pipenv install --dev --system

