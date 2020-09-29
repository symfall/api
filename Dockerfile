FROM python:3
RUN pip install poetry
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY pyproject.toml poetry.lock . /code/
RUN pip install . /code/
COPY . /code/
