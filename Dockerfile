FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
