FROM python:3.12

WORKDIR /parse_them_all
COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv==2025.0.3
RUN pipenv install --dev --system

RUN adduser --disabled-password parse_hero
USER parse_hero
